# alquiler_producto/models/alquiler_producto.py
from odoo import models, fields, api
from odoo.exceptions import UserError
class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Gestión de Servicio de Alquiler de Producto'
    _rec_name = 'garantia_id'
    garantia_id = fields.Many2one('garantia.producto', string='Garantía', required=True)
    customer_id = fields.Many2one('res.partner', string='Cliente',
    related='garantia_id.customer_id', store=True)
    product_id = fields.Many2one('product.product', string='Producto',
    related='garantia_id.product_id', store=True)
    fecha_solicitud = fields.Date(string='Fecha de Solicitud',
    default=fields.Date.context_today, required=True)
    descripcion = fields.Text(string='Descripción del Problema', required=True)
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado')
    ], string='Estado', default='pendiente', required=True)
    fecha_reparacion = fields.Date(string='Fecha de Reparación')
    costo = fields.Float(string='Costo de Reparación')
    fecha_termino = fields.Date(string='Fecha de Término')
    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado == 'en_proceso' and not self.fecha_reparacion:
            self.fecha_reparacion = fields.Date.context_today(self)
    @api.model
    def create(self, vals):
        garantia = self.env['garantia.producto'].browse(vals.get('garantia_id'))
        if garantia.status != 'valid':
            raise UserError('No se puede crear un mantenimiento para una garantía expirada.')
        return super(ServicioMantenimiento, self).create(vals)