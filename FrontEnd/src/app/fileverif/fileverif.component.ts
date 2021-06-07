import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, Inject, Injectable, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { saveAs } from 'file-saver';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Injectable({
  providedIn: 'root'
})
// class pour les requettes GET et POST.
export class ApiStandartization {

  baseurl = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) {

  }

  sendFile(File: any): Observable<any> {

    let formData = new FormData();
    formData.append('file', File, File.name);

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/fileverif/', formData, { headers: header })
  }
}
// interface StandData qui précise les données affichées dans le tableau ainsi que leur type.
export interface VerifyData {
  Visualize: string;
  companyINPUT: string;
  AddressINPUT: string;
  companyOUTPUT: string;
  AddressOUTPUT: string;
}
export interface ViewData {
  companyINPUT: any;
  AddressOUTPUT: any;
  INBUILDINGOUTPUT: any;
  EXTBUILDINGOUTPUT: any;
  POILOGISTICOUTPUT: any;
  ZONEOUTPUT: any;
  HouseNumOUTPUT: any;
  RoadNameOUTPUT: any;
  POBOXOUTPUT: any;
  zipcodeOUTPUT: any;
  cityOUTPUT: any;
  countryOUTPUT: any;
}
@Component({
  selector: 'app-fileverif',
  templateUrl: './fileverif.component.html',
  styleUrls: ['./fileverif.component.css']
})
export class FileverifComponent {
  value: any;
  HiddenSN = false;
  displayedColumns: string[] = ['Visualize', 'companyINPUT', 'AddressINPUT', 'companyOUTPUT', 'AddressOUTPUT'];
  dataSource: MatTableDataSource<VerifyData>;
  df: any;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  Society = new FormControl('');

  filterValues = {
    Society: '',
  };
  constructor(private DATACLEANING: ApiStandartization, public dialog: MatDialog, private router: Router) {
    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
  }

  // function returns tha data of the choosing filter
  createFilter(): (data: any, filter: string) => boolean {
    let filterFunction = function (data: any, filter: any): boolean {
      let searchTerms = JSON.parse(filter);
      return data.companyINPUT.toString().toLowerCase().indexOf(searchTerms.Society.toString().toLowerCase()) !== -1;
    }
    return filterFunction;
  }

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'Visualize', label: 'Visualize', show: true },
    { def: 'companyINPUT', label: 'companyINPUT', show: true },
    { def: 'AddressINPUT', label: 'AddressINPUT', show: true },
    { def: 'companyOUTPUT', label: 'companyOUTPUT', show: true },
    { def: 'AddressOUTPUT', label: 'AddressOUTPUT', show: true },

  ]

  // function that executed the filter
  ExecuteFilter() {
    this.Society.valueChanges
      .subscribe(
        Society => {
          this.filterValues.Society = Society;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
  }
  // Reset table filters
  resetFilters() {
    this.filterValues = {
      Society: ''
    };
    this.dataSource.filter = "";
  }
  // to export data table 
  export() {
    const replacer = (key: any, value: any) => value === null ? '' : value; // specify how you want to handle null values here
    const header = Object.keys(this.dataSource.data[0]);
    let csv = this.dataSource.data.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','));
    csv.unshift(header.join(','));
    let csvArray = csv.join('\r\n');

    var blob = new Blob([csvArray], { type: 'text/csv' })
    saveAs(blob, "Output Data.csv");
  }
  // function executed when file is changed
  fileChangeListener($event: any): void {
    this.df = $event.target.files[0]
  }
  // function executed when user click on standardize button
  createFile = () => {
    if (this.df != null) {
      this.value = 0
      this.DATACLEANING.sendFile(this.df).subscribe(
        data => {
          this.value = 10
          // puts data into the datasource table
          this.dataSource = new MatTableDataSource(data);
          // add filter for data
          this.dataSource.filterPredicate = this.createFilter();
          // execute the filter function
          this.ExecuteFilter();
          // add paginator to the data
          this.dataSource.paginator = this.paginator;
        },
        error => {
          console.log("error ", error);
        }
      );
    }

  }
  // loup element
  async visualize(element: any) {
    // to choose witch data gonna be showing
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '600px',
      data: element
    });
  }
  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }
}
@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog.html',
})
export class DialogOverviewExampleDialog {

  companyINPUT: any;
  AddressOUTPUT: any;
  INBUILDINGOUTPUT: any;
  EXTBUILDINGOUTPUT: any;
  POILOGISTICOUTPUT: any;
  ZONEOUTPUT: any;
  HouseNumOUTPUT: any;
  RoadNameOUTPUT: any;
  POBOXOUTPUT: any;
  zipcodeOUTPUT: any;
  cityOUTPUT: any;
  countryOUTPUT: any;

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: ViewData) {
    
    // to choose data that gonna be showing
    this.companyINPUT = data.companyINPUT
    this.AddressOUTPUT = data.AddressOUTPUT
    this.INBUILDINGOUTPUT = data.INBUILDINGOUTPUT
    this.EXTBUILDINGOUTPUT = data.EXTBUILDINGOUTPUT
    this.POILOGISTICOUTPUT = data.POILOGISTICOUTPUT
    this.ZONEOUTPUT = data.ZONEOUTPUT
    this.HouseNumOUTPUT = data.HouseNumOUTPUT
    this.RoadNameOUTPUT = data.RoadNameOUTPUT
    this.POBOXOUTPUT = data.POBOXOUTPUT
    this.zipcodeOUTPUT = data.zipcodeOUTPUT
    this.cityOUTPUT = data.cityOUTPUT
    this.countryOUTPUT = data.countryOUTPUT

  }

  onNoClick(): void {
    this.dialogRef.close();
  }

}