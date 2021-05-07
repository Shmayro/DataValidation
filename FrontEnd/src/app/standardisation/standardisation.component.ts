import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatTableDataSource } from '@angular/material/table';
import { merge, Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';


@Injectable({
  providedIn: 'root'
})
export class ApiStandartization {
  baseurl = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) { }

  sendAddress(address): Observable<any> {
    const body = { addressU: address.AddressU };
    return this.http.get(this.baseurl + '/standardisation?Address=' + address.addressU, { responseType: "json" });

  }
}
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
}
@Component({
  selector: 'app-standardisation',
  templateUrl: './standardisation.component.html',
  styleUrls: ['./standardisation.component.css'],
  providers: [ApiStandartization],
})
export class StandardisationComponent implements OnInit {
  dataSource: MatTableDataSource<StandData>;
  displayedColumns: string[] = ['INBUILDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY',];
  selectedAddress: any;
  constructor(private DATACLEANING: ApiStandartization) {
    this.dataSource = new MatTableDataSource([]);
    this.selectedAddress = { addressU: '' };
  }

  createAdress = () => {
    this.DATACLEANING.sendAddress(this.selectedAddress).subscribe(
      data => {
        this.dataSource = new MatTableDataSource(data);
        this.execute();
        console.log(this.dataSource)
      },
      error => {
        console.log(this.selectedAddress)
        console.log("error ", error);
      }
    );
  }

  execute(){
    let c1: Observable<boolean> = this.INBUILDING.valueChanges;
    let c2: Observable<boolean> = this.EXTBUILDING.valueChanges;
    let c3: Observable<boolean> = this.POI_LOGISTIC.valueChanges;
    let c4: Observable<boolean> = this.ZONE.valueChanges;
    let c5: Observable<boolean> = this.HOUSENUM.valueChanges;
    let c6: Observable<boolean> = this.ROADNAME.valueChanges;
    let c7: Observable<boolean> = this.POBOX.valueChanges;
    let c8: Observable<boolean> = this.ZIPCODE.valueChanges;
    let c9: Observable<boolean> = this.CITY.valueChanges;
    let c10: Observable<boolean> = this.COUNTRY.valueChanges;
    merge(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10).subscribe(v => {
      this.columnDefinitions[0].show = this.INBUILDING.value;
      this.columnDefinitions[1].show = this.EXTBUILDING.value;
      this.columnDefinitions[2].show = this.POI_LOGISTIC.value;
      this.columnDefinitions[3].show = this.ZONE.value;
      this.columnDefinitions[4].show = this.HOUSENUM.value;
      this.columnDefinitions[5].show = this.ROADNAME.value;
      this.columnDefinitions[6].show = this.POBOX.value;
      this.columnDefinitions[7].show = this.ZIPCODE.value;
      this.columnDefinitions[8].show = this.CITY.value;
      this.columnDefinitions[9].show = this.COUNTRY.value;
      console.log(this.columnDefinitions);
    });
  }
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
    COUNTRY: new FormControl(true)
  });

  INBUILDING = this.form.get('INBUILDING');
  EXTBUILDING = this.form.get('EXTBUILDING');
  POI_LOGISTIC = this.form.get('POI_LOGISTIC');
  ZONE = this.form.get('ZONE');
  HOUSENUM = this.form.get('HOUSENUM');
  ROADNAME = this.form.get('ROADNAME');
  POBOX = this.form.get('POBOX');
  ZIPCODE = this.form.get('ZIPCODE');
  CITY = this.form.get('CITY');
  COUNTRY = this.form.get('COUNTRY');

  /**
     * Control column ordering and which columns are displayed.
     */

  columnDefinitions = [
    { def: 'INBUILDING', label: 'INBUILDING', show: this.INBUILDING.value },
    { def: 'EXTBUILDING', label: 'EXTBUILDING', show: this.EXTBUILDING.value },
    { def: 'POI_LOGISTIC', label: 'POI_LOGISTIC', show: this.POI_LOGISTIC.value },
    { def: 'ZONE', label: 'ZONE', show: this.ZONE.value },
    { def: 'HOUSENUM', label: 'HOUSENUM', show: this.HOUSENUM.value },
    { def: 'ROADNAME', label: 'ROADNAME', show: this.ROADNAME.value },
    { def: 'POBOX', label: 'POBOX', show: this.POBOX.value },
    { def: 'ZIPCODE', label: 'ZIPCODE', show: this.ZIPCODE.value },
    { def: 'CITY', label: 'CITY', show: this.CITY.value },
    { def: 'COUNTRY', label: 'COUNTRY', show: this.COUNTRY.value }
  ]

  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }

  ngAfterViewInit() {
    
  }
  ngOnInit(): void {
  }

}
