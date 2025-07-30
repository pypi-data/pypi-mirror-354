import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

class FEFset:
    def __init__(
        self, app=None, frontend='bootstrap4', url_prefix='/front',
            include_footer=False, role_protection=False, test=False
    ):
        """
        App configuration keys that should be set:
            FEFSET_LOGO_URL: relative url to the logo that should be displayed
            FEFSET_BRAND_NAME: brand name

        Args:
            app: flask.Flask
                The flask application
            frontend: str
                The frontend frameworks, choose between bootstrap4 and bootstrap5
            url_prefix: str
                The blueprint prefix, TODO check if it can be removed
            include_footer: bool
                Include footer in page
            test: bool
                If True, only for testing
            role_protection: bool
                If True, enable role protection. Requires Flask-IAM
        
        Example:
            app.config['FEFSET_BRAND_NAME'] = 'THE BRAND'
        """
        self.frontend = frontend
        self.nav_menu = []
        self.side_menu = []
        self.settings = {'side_menu_name':''}
        self.include_footer = include_footer
        self.url_prefix = url_prefix
        self.role_protection = role_protection

        self.blueprint = Blueprint(
            'fef_blueprint', __name__,
            url_prefix=url_prefix,
            template_folder=os.path.join('templates', self.frontend),
            static_folder = os.path.join('static', self.frontend)
        )
        if test:
            self.blueprint.add_url_rule("/", 'fef', view_func=self.fef_index, methods=['GET'])
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.globals.update({
            "nav_items": self.nav_menu_protected,
            "side_nav_items": self.side_menu_protected,
            "include_footer":  self.include_footer,
            "navconfig": self.settings,
            "role_protection": self.role_protection
            #"navconfig": app.config.get_namespace('FEFSET_')
        })
        if self.frontend.startswith('bootstrap'):
            from flask_bootstrap import Bootstrap
            self.bootstrap = Bootstrap(app)
        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)
        app.extensions['fefset'] = self

    def fef_index(self):
        flash(f"'{self.frontend}' active")
        return render_template('base.html', title='Flask-FEFset for setting your frontend')

    def add_menu_entry(self, name, url, submenu=None, role=False):
        if submenu:
            for sm_ix, nav_item in enumerate(self.nav_menu):
                if nav_item['name'] == submenu:
                    break
            if self.nav_menu[sm_ix]['name'] != submenu:
                self.add_submenu(submenu)
                sm_ix+=1
            nav_menu = self.nav_menu[sm_ix]['nav_items']
        else: nav_menu = self.nav_menu
        nav_menu.append({'name':name,'url':url,'role':role})

    def add_submenu(self, name, url=None, role=False):
        self.nav_menu.append({'name':name,'url':url,'role':role,'nav_items':[]})

    def add_side_menu_entry(self, name, url, role=False):
        self.side_menu.append({'name':name,'url':url,'role':role})

    def nav_menu_protected(self):
        if self.role_protection:
            from flask_iam.utils import check_user_role
            nav_menu = [
                {
                    'name': nmi['name'], 'url': nmi['url'], 'role': nmi['role'],
                    'nav_items': [
                        snmi for snmi in nmi['nav_items']
                        if check_user_role(snmi['role'])
                    ]
                } if 'nav_items' in nmi
                else nmi
                for nmi in self.nav_menu
                if check_user_role(nmi['role'])
            ]
        else: nav_menu = self.nav_menu
        return nav_menu

    def side_menu_protected(self):
        if self.role_protection:
            from flask_iam.utils import check_user_role
            side_menu = [
                smi for smi in self.side_menu
                if check_user_role(smi['role'])
            ]
        else: side_menu = self.side_menu
        return side_menu
