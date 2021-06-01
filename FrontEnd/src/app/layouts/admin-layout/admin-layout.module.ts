import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AdminLayoutRoutes } from './admin-layout.routing';
import { DashboardComponent } from '../../dashboard/dashboard.component';
import { UserProfileComponent } from '../../user-profile/user-profile.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { StandardisationComponent } from 'app/standardisation/standardisation.component';
import {UnitverifComponent} from 'app/unitverif/unitverif.component'
import {FileverifComponent} from 'app/fileverif/fileverif.component'
import { MapsComponent } from '../../maps/maps.component';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatRippleModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTableExporterModule } from 'mat-table-exporter';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatExpansionModule } from '@angular/material/expansion';
import { HomeComponent } from 'app/home/home.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSlideToggleModule } from '@angular/material/slide-toggle'
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner'
import { MatSortModule} from '@angular/material/sort'
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { SafePipe } from '../../dashboard/safe.pipe';

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule,
    MatRippleModule,
    MatDialogModule,
    MatSortModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatMenuModule,
    MatTooltipModule,
    MatTableModule,
    MatPaginatorModule,
    MatExpansionModule,
    MatTableExporterModule,
    MatCheckboxModule,
    MatSlideToggleModule,
  ],
  declarations: [
    SafePipe,
    HomeComponent,
    DashboardComponent,
    UserProfileComponent,
    TableListComponent,
    StandardisationComponent,
    MapsComponent,
    UnitverifComponent,
    FileverifComponent,
  ]
})

export class AdminLayoutModule { }
