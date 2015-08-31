from openerp.osv import fields, osv

class addsol_product_template(osv.osv):
    _inherit = 'product.template'
    _columns = {
        'q_a_required': fields.boolean("QA Required",help = "Tick if this product requires Quality check after arrival"),
        'name_1': fields.char('Name1',help = "Synonym 1"),
        'name_2': fields.char('Name2',help = "Synonym 2"),
        'name_3': fields.char('Name3',help = "Synonym 3"),
        'name_4': fields.char('CAS',help = "CAS #"),
    }
class addsol_product_product(osv.osv):
    _inherit = 'product.product'
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        #name search method to search the product by using synonyms
        filter_domain = ['|','|','|','|',('name','ilike',name),('name_1','ilike',name),('name_2','ilike',name),('name_3','ilike',name),('name_4','ilike',name)]
        for domain in filter_domain:
            args.append(domain)
        ids = self.search(cr, user, filter_domain, context=context)
        return self.name_get(cr, user, ids, context)

    def name_get(self, cr, user, ids, context=None):
        result = super(addsol_product_product, self).name_get(cr, user, ids, context)
        result2 = []
        for res in result:
            namelist = []
            record = self.browse(cr, user, res[0], context)
            if record.name_1:
                namelist.append(record.name_1)
            if record.name_2:
                namelist.append(record.name_2)
            if record.name_3:
                namelist.append(record.name_3)
            if record.name_4:
                namelist.append(record.name_4)
            if namelist:
                new_name = " / ".join(namelist)
                temp = res[1] + " (" + new_name + ")"
                result2.append((res[0],temp))
        if result2:
            return result2
        return result
