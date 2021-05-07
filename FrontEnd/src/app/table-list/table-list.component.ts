import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { NgxCsvParser } from 'ngx-csv-parser';
import { NgxCSVParserError } from 'ngx-csv-parser';
import DataFrame from 'dataframe-js';
import * as FileSaver from 'file-saver';
import { parseHostBindings } from '@angular/compiler';
import { HttpRequest } from '@angular/common/http';

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

    return this.http.post(this.baseurl + '/table-list/', formData,{ headers: header })
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

  HiddenSN = false;
  HiddenCity = false;
  HiddenCode = false;
  HiddenCountry = false;

  displayedColumns: string[] = ['SOCIETY_NAME', 'INBUIDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY'];
  dataSource: MatTableDataSource<StandData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  SOCIETY_NAME = new FormControl('');
  ZIPCODE = new FormControl('');
  CITY = new FormControl('');
  COUNTRY = new FormControl('');
  df;

  filterValues = {
    SOCIETY_NAME: '',
    ZIPCODE: '',
    CITY: '',
    COUNTRY: ''
  };

  constructor(private DATACLEANING: ApiStandartization) {

    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
    this.dataSource.filterPredicate = this.createFilter();

  }

  createFilter(): (data: any, filter: string) => boolean {
    let filterFunction = function (data, filter): boolean {
      let searchTerms = JSON.parse(filter);
      return data.SOCIETY_NAME.toLowerCase().indexOf(searchTerms.SOCIETY_NAME) !== -1
        && data.ZIPCODE.toString().toLowerCase().indexOf(searchTerms.ZIPCODE) !== -1
        && data.CITY.toLowerCase().indexOf(searchTerms.CITY) !== -1
        && data.COUNTRY.toLowerCase().indexOf(searchTerms.COUNTRY) !== -1;
    }
    return filterFunction;
  }

  ngOnInit() {
    this.SOCIETY_NAME.valueChanges
      .subscribe(
        SOCIETY_NAME => {
          this.filterValues.SOCIETY_NAME = SOCIETY_NAME;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
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
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    
  }

  @ViewChild('fileImportInput') fileImportInput: any;

  fileChangeListener($event: any): void {
    console.log($event.target.files[0])
    this.df = $event.target.files[0]
  }
  createFile = () => {
    this.DATACLEANING.sendFile(this.df).subscribe(
      data => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.filterPredicate = this.createFilter();
        this.ngOnInit();
        this.dataSource.paginator = this.paginator;
        //this.dataSource.sort = this.sort;
        console.log(this.dataSource)
      },
      error => {
        console.log("error ", error);
      }
    );
  }
}