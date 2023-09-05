from dbfread import FieldParser

#sometimes are errors in date fields, so return the raw value
class stringdates(FieldParser):
  def parseD(self, field, data):
    # Return strings reversed.
    return str(data.rstrip(b' 0').decode())