import gc
import os.path as osp
import tempfile
import subprocess

import click

import xml.etree.ElementTree as xml_parser

from PyPDF2 import PdfFileReader, PdfFileWriter

from inkscape_pages import separate_layers

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


@click.command()
@click.option('--output', default=None, type=click.Path(exists=False))
@click.argument('svg', type=click.File('rb'))
def cli(output, svg):

    # if there is no output we use the same base name as the svg file
    # and put a pdf extension on it
    if output is None:
        output = osp.join(
            osp.dirname(svg.name),
            '.'.join(osp.splitext(osp.basename(svg.name))[0:-1]) + ".pdf"
        )

    # rad and parse
    svg_str = svg.read()
    svg_etree = xml_parser.fromstring(svg_str)
    del svg_str
    gc.collect()

    # then make a new svg doc for each layer
    page_etrees = separate_layers(svg_etree)
    del svg_etree
    gc.collect()

    # for each slide serialize to xml
    page_svg_strs = [xml_parser.tostring(page) for page in page_etrees]

    # make a temporary directory to put all intermediate files in
    with tempfile.TemporaryDirectory() as tmpdir:

        # paths for tmp files
        page_svg_fnames = [osp.join(tmpdir, 'page_{}.svg'.format(i))
                           for i in range(len(page_svg_strs))]

        # write the page files
        for i, page_svg_fname in enumerate(page_svg_fnames):
            with open(page_svg_fname, 'wb') as wf:
                wf.write(page_svg_strs[i])


        # make paths for the intermediate pdfs
        page_pdf_fnames = [osp.join(tmpdir, 'page_{}.pdf'.format(i))
                           for i in range(len(page_svg_strs))]

        # then convert them to pdfs with the inkscape command
        for i, page_pdf_fname in enumerate(page_pdf_fnames):

            subprocess.run(['inkscape',
                            '--export-filename={}'.format(page_pdf_fname),
                            page_svg_fnames[i]
            ])

        # then combine them using the pdf libarary
        merge_pdfs(page_pdf_fnames, output)

        click.echo("Wrote slideshow pdf to: {}".format(output))


if __name__ == "__main__":

    cli()

