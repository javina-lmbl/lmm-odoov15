# -*- coding: utf-8 -*-
{
    'name': 'Logica Mobile Mexico',
    'description': 'Logica Mobile Mexico module for internal processes',
    'author': 'LMM',
    'application': True,
    'license': "AGPL-3",
    'website': 'https://www.logicamobilemexico.mx',
    'category': "Services/Lmm",
    'version': '15.0.1.0.0',
    'depends': [
        'base',
        'stock',
        'contacts',
        'account',        
        'crm',
        'sale_subscription',
        'helpdesk',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/main_menu.xml',
        'views/accessory.xml',
        'views/cell_chip.xml',
        'views/device.xml',
        'views/platforms_list.xml',
        'views/vehicle_type_list.xml',
        'views/characterization.xml',
        'views/characterization_detail.xml',
        'views/fuel_tank.xml',
        'views/fuel_sensor.xml',
        'views/vehicle.xml',
        'views/calibration_results.xml',
        'views/calibration.xml',
        'views/fuel_test_sample.xml',
        'views/fuel_test.xml',
        'views/account.xml',
        'views/load_division.xml',
        'views/step_load.xml',
    ],
}
