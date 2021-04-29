import { Routes } from '@angular/router';

import { DashboardComponent } from '../../dashboard/dashboard.component';
import { UserProfileComponent } from '../../user-profile/user-profile.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { MapsComponent } from '../../maps/maps.component';
import { StandardisationComponent } from 'app/standardisation/standardisation.component';
import { HomeComponent } from 'app/home/home.component'

export const AdminLayoutRoutes: Routes = [
    { path: 'dashboard', component: DashboardComponent },
    { path: 'user-profile', component: UserProfileComponent },
    { path: 'table-list', component: TableListComponent },
    { path: 'maps', component: MapsComponent },
    { path: 'standardisation', component: StandardisationComponent },
    { path: 'home', component: HomeComponent },
];
