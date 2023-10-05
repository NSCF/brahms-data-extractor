from dbfread import FieldParser, InvalidValue

#sometimes there are errors in date fields, so return the raw value
class stringdates(FieldParser):
  def parseD(self, field, data):
    return str(data.rstrip(b' 0').decode())
  
class genericParser(FieldParser):
  def parse(self, field, data):
    try:
      return FieldParser.parse(self, field, data)
    except ValueError:
      return str(data.decode())