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
@click.option('--export-dpi', default=96, help="DPI used when rasterizing filters, higher DPI improves the quality of the output, but also the file size. A Good high value is 300 (DPI). Default is 96 (DPI)")
@click.option('--crop-to-content', is_flag=True, help="Each separate layer is cropped to its content so there will be no extra space")
@click.argument('svg', type=click.File('rb'))
def cli(output, crop_to_content, export_dpi, svg):

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

        if crop_to_content:
            for i, page_svg_fname in enumerate(page_svg_fnames):
                subprocess.run(['inkscape', '-g', '--batch-process', '--verb', "FitCanvasToDrawing;FileSave;FileClose", page_svg_fname])

        # make paths for the intermediate pdfs
        page_pdf_fnames = [osp.join(tmpdir, 'page_{}.pdf'.format(i))
                           for i in range(len(page_svg_strs))]

        # then convert them to pdfs with the inkscape command
        for i, page_pdf_fname in enumerate(page_pdf_fnames):

            subprocess.run(['inkscape',
                            '--export-dpi={}'.format(export_dpi),
                            '--export-filename={}'.format(page_pdf_fname),
                            page_svg_fnames[i]
            ])

        # then combine them using the pdf libarary
        merge_pdfs(page_pdf_fnames, output)

        click.echo("Wrote slideshow pdf to: {}".format(output))


if __name__ == "__main__":

    cli()

