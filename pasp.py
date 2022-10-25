from PyPDF2 import PdfWriter, PdfReader
import os
import time

reader = PdfReader('tpp.pdf')
print(reader.pages[0].extractText().split('\n'))



# path = os.path.join(os.path.abspath(os.curdir), 'qwe')
#
# for j in os.listdir(path):
#     if j.endswith('.pdf') and not j.startswith('after') and not j.endswith('.py'):
#         reader = PdfReader(os.path.join(path, j), 'rb')
#         writer = PdfWriter()
#         after = PdfReader(os.path.join(path, 'after.pdf'), 'rb')
#         meta = reader.metadata
#
#         for i in range(len(reader.pages) - 1):
#             writer.add_page(reader.pages[i])
#
#         writer.add_page(after.pages[0])
#         writer.add_metadata(meta)
#         with open(os.path.join(os.path.abspath(os.curdir), 'rdy', j), 'wb') as f:
#             writer.write(f)
#             print(f'file-{j} Success')
#             time.sleep(0.5)
