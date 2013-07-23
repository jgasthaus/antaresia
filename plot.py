from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

def save_figure(fig, filename, path = None):
  # We save in PDF, let's try to write some additional metadata
  if path == None:
    path = os.getcwd()
  pdf = PdfPages(path + "/" + filename)
  pdf.savefig(fig)
  pdf_metadata = pdf.infodict()
  path = os.getcwd()
  fn =  path + '/' + sys._current_frames().values()[-1].f_back.f_code.co_filename
  pdf_metadata['Subject'] = "Created by file %s" % (fn, )
  pdf.close()
  os.chdir(path)
  os.system("pdfcrop " + filename)


