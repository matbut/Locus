import logging
from datetime import datetime

from database.models import ImportedArticle


def upload(file_data):
    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    for i, line in enumerate(lines[1:]):
        if len(line) == 0:
            continue
        fields = line.split(",")
        try:
            article = ImportedArticle(page=fields[0], date=datetime.strptime(fields[1], '%Y-%m-%d'), link=fields[2],
                                      title=fields[3],
                                      content=fields[4])
            article.save()
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            pass



