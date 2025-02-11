# alquiler_producto/models/alquiler_producto.py
from odoo import models, fields, api
from odoo.exceptions import UserError

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Gestión de Alquiler de Productos'

    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    producto_id = fields.Many2one('product.product', string='Producto', required=True)
    fecha_inicio = fields.Date(string='Fecha de Inicio', default=fields.Date.context_today, required=True)
    fecha_fin = fields.Date(string='Fecha de Fin', compute='_compute_fecha_fin', store=True)
    estado = fields.Selection([
        ('en_alquiler', 'En Alquiler'),
        ('entregado', 'Entregado'),
        ('no_entregado', 'No Entregado')
    ], string='Estado', default='en_alquiler', required=True)
    observaciones = fields.Text(string='Observaciones')

    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        for record in self:
            if record.fecha_inicio:
                record.fecha_fin = fields.Date.add(record.fecha_inicio, days=30)

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id and self.producto_id.qty_available <= 0:
            raise UserError('El producto no está disponible para alquiler.')

    @api.model
    def _cron_verificar_estado(self):
        alquileres = self.search([('estado', '=', 'en_alquiler')])
        for alquiler in alquileres:
            if alquiler.fecha_fin and fields.Date.today() > alquiler.fecha_fin:
                alquiler.estado = 'no_entregado'