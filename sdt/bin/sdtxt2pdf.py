#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module make a PDF file from a text file."""

import sys
import argparse
import reportlab.lib.pagesizes
import reportlab.graphics.shapes
import reportlab.pdfgen

def run(ifile,opathname,draw_frame):
    t2p = Txt2pdf(opathname, draw_frame=draw_frame)
    ifile.seek(0)
    for iline in ifile.readlines():
        t2p.line(iline.rstrip())
    t2p.finish()

def err(str):
    print >>sys.stderr, "txt2pdf: ", str, "\n";

def mm2pt (mm):
    return mm / 25.4 * 72;

class Txt2pdf:
    def __init__(self, file_name, **kwargs):
        self.prm = kwargs

        # FIXME hard-coded page sz
        self.canvas = reportlab.pdfgen.canvas.Canvas(file_name, pagesize=reportlab.lib.pagesizes.A4)
        # FIXME hard-coded page dimensions
        self.sheet_w_mm = 210
        self.sheet_h_mm = 297
        self.margin_w_mm = 15
        self.margin_h_mm = 15
        self.page_w_mm = self.sheet_w_mm - 2 * self.margin_w_mm
        self.page_h_mm = self.sheet_h_mm - 2 * self.margin_h_mm

        self.font_nm = 'Courier'
        self.font_sz_pt = 10

        self.page_nums = True

        # Coordinates of edges of printed area
        self.xl_pt = mm2pt(self.margin_w_mm)
        self.xc_pt = mm2pt(self.margin_w_mm + (self.sheet_w_mm - 2 * self.margin_w_mm) / 2)
        self.xr_pt = mm2pt(self.sheet_w_mm - self.margin_w_mm)
        self.yb_pt = mm2pt(self.margin_h_mm)
        self.yt_pt = mm2pt(self.sheet_h_mm - self.margin_h_mm)

        self.first_line_y_pt = self.yt_pt - self.font_sz_pt
        self.end_line_y_pt = self.yb_pt
        if self.page_nums:
            self.end_line_y_pt += 2 * self.font_sz_pt

        self.top_of_page = True
        self.page_started = False
        self.page_num = 1

    def line(self, str):
        if self.top_of_page:
            self.top_of_page = False
            self.page_started = True
            if ('draw_frame' in self.prm and self.prm['draw_frame']):
                self.canvas.setLineWidth(0.2)
                self.canvas.setDash([1, 1], 0)
                self.canvas.line(self.xl_pt, self.yt_pt, self.xr_pt, self.yt_pt)
                self.canvas.line(self.xr_pt, self.yt_pt, self.xr_pt, self.yb_pt)
                self.canvas.line(self.xr_pt, self.yb_pt, self.xl_pt, self.yb_pt)
                self.canvas.line(self.xl_pt, self.yb_pt, self.xl_pt, self.yt_pt)
            self.canvas.setFont(self.font_nm, self.font_sz_pt)
            self.x_pt = self.xl_pt
            self.y_pt = self.first_line_y_pt
        self.canvas.drawString(self.x_pt, self.y_pt, str)
        # Move font_sz_pt points down
        self.y_pt -= self.font_sz_pt
        if self.y_pt < self.end_line_y_pt:
            self.page_end()

    def page_end(self):
        if self.page_nums:
            self.canvas.drawCentredString(self.xc_pt, self.yb_pt, str(self.page_num))
            self.page_num += 1
        self.canvas.showPage()
        self.page_started = False
        self.top_of_page = True

    def finish(self):
        if self.page_started:
            self.page_end()
        self.canvas.save()

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-f','--frame',action='store_true')
    parser.add_argument('-o','--outfile',required=True)
    args=parser.parse_args()

    ifile = open(args.infile, "r")
    run(ifile,args.outfile,args.frame)
    ifile.close()

    # FIXME catch and report errors

    sys.exit(0)
