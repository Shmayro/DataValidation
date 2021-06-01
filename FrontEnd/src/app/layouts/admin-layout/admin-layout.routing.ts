import { Routes } from '@angular/router';

import { DashboardComponent } from '../../dashboard/dashboard.component';
import { UserProfileComponent } from '../../user-profile/user-profile.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { MapsComponent } from '../../maps/maps.component';
import { StandardisationComponent } from 'app/standardisation/standardisation.component';
import { HomeComponent } from 'app/home/home.component'
import { UnitverifComponent } from 'app/unitverif/unitverif.component';
import { FileverifComponent } from 'app/fileverif/fileverif.component';

export const AdminLayoutRoutes: Routes = [
    { path: 'dashboard', component: DashboardComponent },
    { path: 'dashboard/:dataFrame', component: DashboardComponent },
    { path: 'user-profile', component: UserProfileComponent },
    { path: 'table-list', component: TableListComponent },
    { path: 'table-list/stat', component: TableListComponent },
    { path: 'maps', component: MapsComponent },
    { path: 'standardisation', component: StandardisationComponent },
    { path: 'home', component: HomeComponent },
    { path: 'unitverif', component: UnitverifComponent },
    { path: 'fileverif', component: FileverifComponent },
];
