import { Component, Inject, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { merge, Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { saveAs } from 'file-saver';
import * as Highcharts from 'highcharts';
import { Router } from '@angular/router';

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
    return this.http.post(this.baseurl + '/table-list/', formData, { headers: header })
  }

  sendStat(File: any): Observable<any> {
    var header = new HttpHeaders();
    header.append('Content-Type', 'text/plain');
    return this.http.post(this.baseurl + '/table-list/stat/', File, { headers: header })
  }

  getAbrr(element: any): Observable<any> {
    return this.http.get(this.baseurl + '/table-list/abr/?Address=' + element, { responseType: "json" });
  }

  getCorrType(element: any): Observable<any> {
    return this.http.get(this.baseurl + '/table-list/corr/?Address=' + element, { responseType: "json" });
  }
}

// interface StandData qui précise les données affichées dans le tableau ainsi que leur type.
export interface StandData {
  SOCIETY_NAME: string;
  INBUILDING: string;
  EXTBUILDING: string;
  POI_LOGISTIC: string;
  ZONE: string;
  HOUSENUM: string;
  ROADNAME: string;
  POBOX: string;
  ZIPCODE: string;
  CITY: string;
  COUNTRY: string;
  ADDITIONAL: String;
  Statistics: string;
}
@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css'],
  providers: [ApiStandartization]
})

export class TableListComponent {

  renderedData: any;
  dataFrame: any;
  HiddenSN = false;
  HiddenCity = false;
  HiddenCode = false;
  HiddenCountry = false;

  displayedColumns: string[] = ['SOCIETY_NAME', 'INBUILDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY', 'ADDITIONAL', 'Statistics'];
  dataSource: MatTableDataSource<StandData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  Society = new FormControl('');
  ZipCode = new FormControl('');
  City = new FormControl('');
  Country = new FormControl('');
  element: any;
  df: any;
  options: any
  nbAbr: number = 0;
  nbCorr: number = 0;

  filterValues = {
    Society: '',
    ZipCode: '',
    City: '',
    Country: ''
  };
  value: number;

  constructor(private DATACLEANING: ApiStandartization, public dialog: MatDialog, private router: Router) {

    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);

  }
  // function returns tha data of the choosing filter
  createFilter(): (data: any, filter: string) => boolean {
    let filterFunction = function (data: any, filter: any): boolean {
      let searchTerms = JSON.parse(filter);
      return data.company.toString().toLowerCase().indexOf(searchTerms.Society.toString().toLowerCase()) !== -1
        && data.ZIPCODE.toString().toLowerCase().indexOf(searchTerms.ZipCode.toString().toLowerCase()) !== -1
        && data.CITY.toString().toLowerCase().indexOf(searchTerms.City.toString().toLowerCase()) !== -1
        && data.COUNTRY.toString().toLowerCase().indexOf(searchTerms.Country.toString().toLowerCase()) !== -1;
    }
    return filterFunction;
  }
  getNbAbr(element: any) {
    return new Promise(resolve => {
      setTimeout(() => {
        this.DATACLEANING.getAbrr(element.ADDRESS).subscribe(
          data => {
            this.nbAbr = data[0].nb;
            resolve(this.nbAbr)
          }
        )
      }, 100);
    });

  }
  getNbCorr(element: any) {
    return new Promise(resolve => {
      setTimeout(() => {
        this.DATACLEANING.getCorrType(element.ADDRESS).subscribe(
          data => {
            this.nbCorr = data[0].nbtot;
            resolve(this.nbCorr)
          }
        )
      }, 100);
    });
  }
  getOptions(nbAbr: number, nbCorr: number, txt: string) {
    this.options = {
      chart: {
        type: 'column',
      },
      title: {
        text: txt,
      },
      subtitle: {
        text: 'statistics'
      },
      xAxis: {
        type: 'category',
        labels: {
          rotation: -45,
          style: {
            fontSize: '13px',
            fontFamily: 'Verdana, sans-serif'
          }
        }
      },
      yAxis: {
        min: 0,
        title: {
          text: 'Number'
        }
      },
      legend: {
        enabled: false
      },
      tooltip: {
        pointFormat: 'Number : <b>{point.y:.1f}</b>'
      },
      series: [{
        name: 'Champs',
        data: [
          ['Number of abbreviation', nbAbr],
          ['Number of TypeErrorCorrection', nbCorr]
        ],
        dataLabels: {
          enabled: true,
          rotation: -90,
          color: '#FFFFFF',
          align: 'right',
          format: '{point.y:.1f}', // one decimal
          y: 10, // 10 pixels down from the top
          style: {
            fontSize: '13px',
            fontFamily: 'Verdana, sans-serif'
          }
        }
      }]
    }
    return this.options
  }

  // dashboard element
  async dashboardElement(element: any) {
    let nbAbr: any, nbCorr: any

    nbAbr = await this.getNbAbr(element)
    nbCorr = await this.getNbCorr(element)
    let txt = 'Number of abbreviation & TypeErrorCorrection in this adress'
    this.getOptions(nbAbr, nbCorr, txt)

    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '600px',
      data: this.options
    });
    Highcharts.chart('container', this.options)
  }

  // dashboard element
  dashboard() {

    let nbArr = 0
    let nbCorr = 0
    let txt = 'Number of abbreviation & TypeErrorCorrection in all the table'
    for (let index = 0; index < this.dataFrame.length; index++) {
      nbArr += this.dataFrame[index].nbArr
      nbCorr += this.dataFrame[index].nbCorr
    }
    this.getOptions(nbArr, nbCorr, txt)

    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '800px',
      data: this.options
    });
    Highcharts.chart('container', this.options)
  }
  // function that executed the filter
  ExecuteFilter() {
    this.Society.valueChanges
      .subscribe(
        Society => {
          this.filterValues.Society = Society;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.ZipCode.valueChanges
      .subscribe(
        ZipCode => {
          this.filterValues.ZipCode = ZipCode;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.City.valueChanges
      .subscribe(
        City => {
          this.filterValues.City = City;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.Country.valueChanges
      .subscribe(
        Country => {
          this.filterValues.Country = Country;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
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
          this.dataFrame = data;
          // to choose witch data gonna be showing in the table
          this.InitializeVisualization();
          // puts data into the datasource table
          this.dataSource = new MatTableDataSource(data);
          // add filter for data
          this.dataSource.filterPredicate = this.createFilter();
          // execute the filter function
          this.ExecuteFilter();
          // execute the visualisation function
          this.executeVisualisation();
          // put Data into a rendered Data to export
          this.dataSource.connect().subscribe(d => this.renderedData = d);
          // add paginator to the data
          this.dataSource.paginator = this.paginator;
        },
        error => {
          console.log("error ", error);
        }
      );
    }

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

  // Reset table filters
  resetFilters() {
    this.filterValues = {
      Society: '',
      ZipCode: '',
      City: '',
      Country: ''
    };
    this.dataSource.filter = "";
  }

  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
    let c0: Observable<boolean> = this.SOCIETY_NAME.valueChanges;
    let c1: Observable<boolean> = this.INB.valueChanges;
    let c2: Observable<boolean> = this.EXTB.valueChanges;
    let c3: Observable<boolean> = this.POI.valueChanges;
    let c4: Observable<boolean> = this._ZONE.valueChanges;
    let c5: Observable<boolean> = this._HOUSENUM.valueChanges;
    let c6: Observable<boolean> = this._ROADNAME.valueChanges;
    let c7: Observable<boolean> = this._POBOX.valueChanges;
    let c8: Observable<boolean> = this._ZIPCODE.valueChanges;
    let c9: Observable<boolean> = this._CITY.valueChanges;
    let c10: Observable<boolean> = this._COUNTRY.valueChanges;
    let c11: Observable<boolean> = this.ADDITIONAL.valueChanges;
    let c12: Observable<boolean> = this.Statistics.valueChanges;
    merge(c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12).subscribe(v => {
      this.columnDefinitions[0].show = this.SOCIETY_NAME.value;
      this.columnDefinitions[1].show = this.INB.value;
      this.columnDefinitions[2].show = this.EXTB.value;
      this.columnDefinitions[3].show = this.POI.value;
      this.columnDefinitions[4].show = this._ZONE.value;
      this.columnDefinitions[5].show = this._HOUSENUM.value;
      this.columnDefinitions[6].show = this._ROADNAME.value;
      this.columnDefinitions[7].show = this._POBOX.value;
      this.columnDefinitions[8].show = this._ZIPCODE.value;
      this.columnDefinitions[9].show = this._CITY.value;
      this.columnDefinitions[10].show = this._COUNTRY.value;
      this.columnDefinitions[11].show = this.ADDITIONAL.value;
      this.columnDefinitions[12].show = this.Statistics.value;
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'SOCIETY_NAME', label: 'SOCIETY_NAME', show: this.SOCIETY_NAME.value },
      { def: 'INBUILDING', label: 'INBUILDING', show: this.INB.value },
      { def: 'EXTBUILDING', label: 'EXTBUILDING', show: this.EXTB.value },
      { def: 'POI_LOGISTIC', label: 'POI', show: this.POI.value },
      { def: 'ZONE', label: 'ZONE', show: this._ZONE.value },
      { def: 'HOUSENUM', label: 'HOUSENUM', show: this._HOUSENUM.value },
      { def: 'ROADNAME', label: 'ROADNAME', show: this._ROADNAME.value },
      { def: 'POBOX', label: 'POBOX', show: this._POBOX.value },
      { def: 'ZIPCODE', label: 'ZIPCODE', show: this._ZIPCODE.value },
      { def: 'CITY', label: 'CITY', show: this._CITY.value },
      { def: 'COUNTRY', label: 'COUNTRY', show: this._COUNTRY.value },
      { def: 'ADDITIONAL', label: 'ADDITIONAL', show: this.ADDITIONAL.value },
      { def: 'Statistics', label: 'Statistics', show: this.Statistics.value }
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
    SOCIETY_NAME: new FormControl(true),
    INBUILDING: new FormControl(true),
    EXTBUILDING: new FormControl(true),
    POI_LOGISTIC: new FormControl(true),
    ZONE: new FormControl(true),
    HOUSENUM: new FormControl(true),
    ROADNAME: new FormControl(true),
    POBOX: new FormControl(true),
    ZIPCODE: new FormControl(true),
    CITY: new FormControl(true),
    COUNTRY: new FormControl(true),
    ADDITIONAL: new FormControl(true),
    Statistics: new FormControl(true)
  });

  // geting the checkBox
  SOCIETY_NAME = this.form.get('SOCIETY_NAME');
  INB = this.form.get('INBUILDING');
  EXTB = this.form.get('EXTBUILDING');
  POI = this.form.get('POI_LOGISTIC');
  _ZONE = this.form.get('ZONE');
  _HOUSENUM = this.form.get('HOUSENUM');
  _ROADNAME = this.form.get('ROADNAME');
  _POBOX = this.form.get('POBOX');
  _ZIPCODE = this.form.get('ZIPCODE');
  _CITY = this.form.get('CITY');
  _COUNTRY = this.form.get('COUNTRY');
  ADDITIONAL = this.form.get('ADDITIONAL');
  Statistics = this.form.get('Statistics');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'SOCIETY_NAME', label: 'SOCIETY_NAME', show: this.SOCIETY_NAME.value },
    { def: 'INBUILDING', label: 'INBUILDING', show: this.INB.value },
    { def: 'EXTBUILDING', label: 'EXTBUILDING', show: this.EXTB.value },
    { def: 'POI_LOGISTIC', label: 'POI', show: this.POI.value },
    { def: 'ZONE', label: 'ZONE', show: this._ZONE.value },
    { def: 'HOUSENUM', label: 'HOUSENUM', show: this._HOUSENUM.value },
    { def: 'ROADNAME', label: 'ROADNAME', show: this._ROADNAME.value },
    { def: 'POBOX', label: 'POBOX', show: this._POBOX.value },
    { def: 'ZIPCODE', label: 'ZIPCODE', show: this._ZIPCODE.value },
    { def: 'CITY', label: 'CITY', show: this._CITY.value },
    { def: 'COUNTRY', label: 'COUNTRY', show: this._COUNTRY.value },
    { def: 'ADDITIONAL', label: 'ADDITIONAL', show: this.ADDITIONAL.value },
    { def: 'Statistics', label: 'Statistics', show: this.Statistics.value }
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }

  // Get Statistics forms
  statistics() {
    this.DATACLEANING.sendStat(JSON.parse(JSON.stringify(this.dataFrame))).subscribe(
      data => {

        console.log("lets go")
        //data=data.substring(15);
        this.router.navigate(['dashboard'], { queryParams: { data: data } });
      });
    /*let navigationExtras: NavigationExtras = {
        queryParams: {
          "file": JSON.stringify(this.dataFrame)
        }
      }
      this.router.navigate(['dashboard'], navigationExtras);*/
  }
}
@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog.html',
})
export class DialogOverviewExampleDialog {

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: StandData) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

}