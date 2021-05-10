import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { merge, Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { ngxCsv } from 'ngx-csv/ngx-csv';

@Injectable({
  providedIn: 'root'
})
export class ApiStandartization {
  baseurl = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) { }

  sendFile(File): Observable<any> {

    let formData = new FormData();
    formData.append('file', File, File.name);

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');

    return this.http.post(this.baseurl + '/table-list/', formData, { headers: header })
  }
}
export interface StandData {
  SOCIETY_NAME: string;
  INBUIDING: string;
  EXTBUILDING: string;
  POI_LOGISTIC: string;
  ZONE: string;
  HOUSENUM: string;
  ROADNAME: string;
  POBOX: string;
  ZIPCODE: string;
  CITY: string;
  COUNTRY: string;
}
@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css'],
  providers: [ApiStandartization]
})

export class TableListComponent implements AfterViewInit {

  renderedData: any;

  HiddenSN = false;
  HiddenCity = false;
  HiddenCode = false;
  HiddenCountry = false;

  displayedColumns: string[] = ['INBUIDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY','ADDITIONAL'];
  dataSource: MatTableDataSource<StandData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  //_SOCIETY_NAME = new FormControl('');
  ZIPCODE = new FormControl('');
  CITY = new FormControl('');
  COUNTRY = new FormControl('');

  df;

  filterValues = {
    // _SOCIETY_NAME: '',
    ZIPCODE: '',
    CITY: '',
    COUNTRY: ''
  };

  constructor(private DATACLEANING: ApiStandartization) {

    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
    //this.dataSource.filterPredicate = this.createFilter();

  }

  createFilter(): (data: any, filter: string) => boolean {
    let filterFunction = function (data, filter): boolean {
      let searchTerms = JSON.parse(filter);
      //data.SOCIETY_NAME.toLowerCase().indexOf(searchTerms.SOCIETY_NAME) !== -1 &&
      return data.ZIPCODE.toString().toLowerCase().indexOf(searchTerms.ZIPCODE.toString().toLowerCase()) !== -1
        && data.CITY.toString().toLowerCase().indexOf(searchTerms.CITY.toString().toLowerCase()) !== -1
        && data.COUNTRY.toString().toLowerCase().indexOf(searchTerms.COUNTRY.toString().toLowerCase()) !== -1;
    }
    return filterFunction;
  }

  // function that executed
  ExecuteFilter() {
    /*this._SOCIETY_NAME.valueChanges
      .subscribe(
        SOCIETY_NAME => {
          this.filterValues._SOCIETY_NAME = SOCIETY_NAME;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )*/
    this.ZIPCODE.valueChanges
      .subscribe(
        ZIPCODE => {
          this.filterValues.ZIPCODE = ZIPCODE;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.CITY.valueChanges
      .subscribe(
        CITY => {
          this.filterValues.CITY = CITY;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.COUNTRY.valueChanges
      .subscribe(
        COUNTRY => {
          this.filterValues.COUNTRY = COUNTRY;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
  }
  ngAfterViewInit() {

  }

// function executed when file is changed
  fileChangeListener($event: any): void {
    console.log($event.target.files[0])
    this.df = $event.target.files[0]
  }

  // function executed when user click on standardize button
  createFile = () => {
    if (this.df != null) {
      this.DATACLEANING.sendFile(this.df).subscribe(
        data => {
          // to choose witch data gonna be showing
          this.InitializeVisualization();
          // puts data into the datasource table
          this.dataSource = new MatTableDataSource(data);
          // add filter for data
          this.dataSource.filterPredicate = this.createFilter();
          //  execute the filter function
          this.ExecuteFilter();
          // execute the visualisation function
          this.executeVisualisation();
          // put Data into a rendered Data to export
          this.dataSource.connect().subscribe(d => this.renderedData = d);
          // add paginator to the data
          this.dataSource.paginator = this.paginator;
          console.log(this.dataSource)
        },
        error => {
          console.log("error ", error);
        }
      );
    }

  }

  // to export data table (not for all data just the showing data)
  export() {
    new ngxCsv(this.renderedData, 'Output');
  }

  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
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
    merge(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11).subscribe(v => {
      this.columnDefinitions[0].show = this.INB.value;
      this.columnDefinitions[1].show = this.EXTB.value;
      this.columnDefinitions[2].show = this.POI.value;
      this.columnDefinitions[3].show = this._ZONE.value;
      this.columnDefinitions[4].show = this._HOUSENUM.value;
      this.columnDefinitions[5].show = this._ROADNAME.value;
      this.columnDefinitions[6].show = this._POBOX.value;
      this.columnDefinitions[7].show = this._ZIPCODE.value;
      this.columnDefinitions[8].show = this._CITY.value;
      this.columnDefinitions[9].show = this._COUNTRY.value;
      this.columnDefinitions[10].show = this.ADDITIONAL.value;
      console.log(this.columnDefinitions);
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'INBUILDING', label: 'INBUILDING', show: this.INB.value },
      { def: 'EXTBUILDING', label: 'EXTBUILDING', show: this.EXTB.value },
      { def: 'POI_LOGISTIC', label: 'POI_LOGISTIC', show: this.POI.value },
      { def: 'ZONE', label: 'ZONE', show: this._ZONE.value },
      { def: 'HOUSENUM', label: 'HOUSENUM', show: this._HOUSENUM.value },
      { def: 'ROADNAME', label: 'ROADNAME', show: this._ROADNAME.value },
      { def: 'POBOX', label: 'POBOX', show: this._POBOX.value },
      { def: 'ZIPCODE', label: 'ZIPCODE', show: this._ZIPCODE.value },
      { def: 'CITY', label: 'CITY', show: this._CITY.value },
      { def: 'COUNTRY', label: 'COUNTRY', show: this._COUNTRY.value },
      { def: 'ADDITIONAL', label: 'ADDITIONAL', show: this.ADDITIONAL.value }
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
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
    ADDITIONAL: new FormControl(true)
  });

  // geting the checkBox
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
  ADDITIONAL=this.form.get('ADDITIONAL');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'INBUILDING', label: 'INBUILDING', show: this.INB.value },
    { def: 'EXTBUILDING', label: 'EXTBUILDING', show: this.EXTB.value },
    { def: 'POI_LOGISTIC', label: 'POI_LOGISTIC', show: this.POI.value },
    { def: 'ZONE', label: 'ZONE', show: this._ZONE.value },
    { def: 'HOUSENUM', label: 'HOUSENUM', show: this._HOUSENUM.value },
    { def: 'ROADNAME', label: 'ROADNAME', show: this._ROADNAME.value },
    { def: 'POBOX', label: 'POBOX', show: this._POBOX.value },
    { def: 'ZIPCODE', label: 'ZIPCODE', show: this._ZIPCODE.value },
    { def: 'CITY', label: 'CITY', show: this._CITY.value },
    { def: 'COUNTRY', label: 'COUNTRY', show: this._COUNTRY.value },
    { def: 'ADDITIONAL', label: 'ADDITIONAL', show: this.ADDITIONAL.value }
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }
}