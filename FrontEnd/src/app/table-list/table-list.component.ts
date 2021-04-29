import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { NgxCsvParser } from 'ngx-csv-parser';
import { NgxCSVParserError } from 'ngx-csv-parser';
import { Location, LocationStrategy, PathLocationStrategy, PopStateEvent } from '@angular/common';

const NAMES: string[] = [
  'Maia', 'Asher', 'Olivia', 'Atticus', 'Amelia', 'Jack', 'Charlotte', 'Theodore', 'Isla', 'Oliver',
  'Isabella', 'Jasper', 'Cora', 'Levi', 'Violet', 'Arthur', 'Mia', 'Thomas', 'Elizabeth'
];

export interface UserData {
  SOCIETY_NAME: string;
  INBUIDING: string;
  EXTBUILDING: string;
  POI_LOGISTIC: string;
  ZONE: string;
  HOUSE_NUM: string;
  ROADNUM: string;
  POBOX: string;
  ZIPCODE: string;
  CITY: string;
  COUNTRY: string;
}
@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css']
})

export class TableListComponent implements AfterViewInit {

  HiddenSN = false; 
  HiddenCity=false;
  HiddenCode=false;
  HiddenCountry=false;
  
  displayedColumns: string[] = ['SOCIETY_NAME', 'INBUIDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSE_NUM', 'ROADNUM', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY'];
  dataSource: MatTableDataSource<UserData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  csvRecords: any[] = [];
  header: boolean = false;

  SOCIETY_NAME = new FormControl('');
  ZIPCODE = new FormControl('');
  CITY = new FormControl('');
  COUNTRY = new FormControl('');

  
  filterValues = {
    SOCIETY_NAME: '',
    ZIPCODE: '',
    CITY: '',
    COUNTRY: ''
  };

  constructor(public location: Location, private ngxCsvParser: NgxCsvParser) {
    // Create 100 users
    const users = Array.from({ length: 100 }, (_, k) => createNewUser(k + 1));

    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource(users);
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
  checkEvent(){
    if (this.HiddenSN==false) {
      this.filterValues.SOCIETY_NAME=''
    }
  }
  ngOnInit() {
    this.SOCIETY_NAME.valueChanges
      .subscribe(
        name => {
          this.filterValues.SOCIETY_NAME = name;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.ZIPCODE.valueChanges
      .subscribe(
        id => {
          this.filterValues.ZIPCODE = id;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.CITY.valueChanges
      .subscribe(
        colour => {
          this.filterValues.CITY = colour;
          this.dataSource.filter = JSON.stringify(this.filterValues);
        }
      )
    this.COUNTRY.valueChanges
      .subscribe(
        pet => {
          this.filterValues.COUNTRY = pet;
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

    const files = $event.srcElement.files;
    this.header = (this.header as unknown as string) === 'true' || this.header === true;

    this.ngxCsvParser.parse(files[0], { header: this.header })
      .pipe().subscribe((result: Array<any>) => {
        console.log('Result', result);
        this.csvRecords = result;
      }, (error: NgxCSVParserError) => {
        console.log('Error', error);
      });
  }
}

/** Builds and returns a new User. */
function createNewUser(SOCIETY_NAME: number): UserData {
  const name = NAMES[Math.round(Math.random() * (NAMES.length - 1))] + ' ' +
    NAMES[Math.round(Math.random() * (NAMES.length - 1))].charAt(0) + '.';

  return {
    SOCIETY_NAME: name,
    INBUIDING: Math.round(Math.random() * 100).toString(),
    EXTBUILDING: Math.round(Math.random() * 100).toString(),
    POI_LOGISTIC: Math.round(Math.random() * 100).toString(),
    HOUSE_NUM: Math.round(Math.random() * 100).toString(),
    POBOX: Math.round(Math.random() * 100).toString(),
    ROADNUM: Math.round(Math.random() * 100).toString(),
    ZONE: Math.round(Math.random() * 100).toString(),
    ZIPCODE: Math.round(Math.random() * 100).toString(),
    CITY: Math.round(Math.random() * 100).toString(),
    COUNTRY: name
  };

}
