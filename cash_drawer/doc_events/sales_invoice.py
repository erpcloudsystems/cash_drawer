def before_insert(doc, method=None):
    doc.set("dc", 0)
