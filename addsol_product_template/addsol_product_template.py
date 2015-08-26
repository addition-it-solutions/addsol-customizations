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
        args.append(('|'))
        args.append(('|'))
        args.append(('|'))
        args.append(('|'))
        args.append(('name','ilike',name))
        args.append(('name_1','ilike',name))
        args.append(('name_2','ilike',name))
        args.append(('name_3','ilike',name))
        args.append(('name_4','ilike',name))
        return super(addsol_product_product,self).name_search(cr, user, '', args=args,operator='ilike', context=context, limit=limit)
