# A "Responsive" Web Application for Standardizing, Verifying and Validating Transport Data

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 1.0.0 and angular 4.x.

## Code scaffolding

Run `ng generate component component-name` to generate a new component or `ng g c component-name`. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.


## Terminal Commands

1. Install NodeJs from [NodeJs Official Page](https://nodejs.org/en).
2. Open Terminal
3. Go to your file project
4. Make sure you have installed [Angular CLI](https://github.com/angular/angular-cli) already. If not, please install.
5. Run in terminal: ```npm install```
6. Run `ng serve --open` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### What's included

Within the download you'll find the following directories and files:

```
DataValidation
├── BackEnd
│   ├── DataValidation
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── StandApp
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   ├── abbreviation.json
│   ├── city_list.csv
│   ├── Input_Stand.csv
│   ├── Input.csv
│   ├── manage.py
├── FrontEnd
│   ├── e2e
│   ├── src
│   │   ├── app
│   │   │   ├── components
│   │   │   │   ├── components.module.ts
│   │   │   │   ├── footer
│   │   │   │   │   ├── footer.component.css
│   │   │   │   │   ├── footer.component.html
│   │   │   │   │   ├── footer.component.spec.ts
│   │   │   │   │   └── footer.component.ts
│   │   │   │   ├── navbar
│   │   │   │   │   ├── navbar.component.css
│   │   │   │   │   ├── navbar.component.html
│   │   │   │   │   ├── navbar.component.spec.ts
│   │   │   │   │   └── navbar.component.ts
│   │   │   │   └── sidebar
│   │   │   │       ├── sidebar.component.css
│   │   │   │       ├── sidebar.component.html
│   │   │   │       ├── sidebar.component.spec.ts
│   │   │   │       └── sidebar.component.ts
│   │   │   ├── dashboard
│   │   │   │   ├── dashboard.component.css
│   │   │   │   ├── dashboard.component.html
│   │   │   │   ├── dashboard.component.spec.ts
│   │   │   │   └── dashboard.component.ts
│   │   │   ├── home
│   │   │   │   ├── home.component.css
│   │   │   │   ├── home.component.html
│   │   │   │   ├── home.component.spec.ts
│   │   │   │   └── home.component.ts
│   │   │   ├── layouts
│   │   │   │   └── admin-layout
│   │   │   │       ├── admin-layout.component.html
│   │   │   │       ├── admin-layout.component.scss
│   │   │   │       ├── admin-layout.component.spec.ts
│   │   │   │       ├── admin-layout.component.ts
│   │   │   │       ├── admin-layout.module.ts
│   │   │   │       └── admin-layout.routing.ts
│   │   │   ├── login
│   │   │   │   ├── login.component.css
│   │   │   │   ├── login.component.html
│   │   │   │   ├── login.component.spec.ts
│   │   │   │   └── login.component.ts
│   │   │   ├── register
│   │   │   │   ├── register.component.css
│   │   │   │   ├── register.component.html
│   │   │   │   ├── register.component.spec.ts
│   │   │   │   └── register.component.ts
│   │   │   ├── standardisation
│   │   │   │   ├── standardisation.component.css
│   │   │   │   ├── standardisation.component.html
│   │   │   │   ├── standardisation.component.spec.ts
│   │   │   │   └── standardisation.component.ts
│   │   │   ├── table-list
│   │   │   │   ├── table-list.component.css
│   │   │   │   ├── table-list.component.html
│   │   │   │   ├── table-list.component.spec.ts
│   │   │   │   └── table-list.component.ts
│   │   │   └── user-profile
│   │   │   │   ├── user-profile.component.css
│   │   │   │   ├── user-profile.component.html
│   │   │   │   ├── user-profile.component.spec.ts
│   │   │   │   └── user-profile.component.ts
│   │   │   ├── app.component.css
│   │   │   ├── app.component.html
│   │   │   ├── app.component.spec.ts
│   │   │   ├── app.component.ts
│   │   │   ├── app.module.ts
│   │   │   ├── app.routing.ts
│   │   ├── assets
│   │   │   ├── css
│   │   │   │   └── demo.css
│   │   │   ├── img
│   │   │   └── scss
│   │   │       ├── core
│   │   │       └── material-dashboard.scss
│   │   ├── environments
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── main.ts
│   │   ├── polyfills.ts
│   │   ├── styles.css
│   │   ├── test.ts
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.spec.json
│   │   └── typings.d.ts
│   ├── angular.json
│   ├── CHANGELOG.md
│   ├── karma.conf.js
│   ├── package-lock.json
│   ├── package.json
│   ├── protractor.conf.js
│   ├── README.md
│   ├── tsconfig.json
│   ├── tslint.json

```