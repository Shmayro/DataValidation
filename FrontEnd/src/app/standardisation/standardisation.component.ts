import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
export class StandardisationComponent {
  dataSource: MatTableDataSource<StandData>;
  displayedColumns: string[] = ['INBUILDING', 'EXTBUILDING', 'POI_LOGISTIC', 'ZONE', 'HOUSENUM', 'ROADNAME', 'POBOX', 'ZIPCODE', 'CITY', 'COUNTRY','ADDITIONAL'];
  selectedAddress: any;

  constructor(private DATACLEANING: ApiStandartization) {
    this.dataSource = new MatTableDataSource([]);
    this.selectedAddress = { addressU: '' };
  }

  createAdress = () => {
    console.log(this.selectedAddress)
    this.DATACLEANING.sendAddress(this.selectedAddress).subscribe(
      data => {
        // to choose witch data gonna be showing
        this.InitializeVisualization();
        // puts data into the datasource table
        this.dataSource = new MatTableDataSource(data);
        // execute the visualisation function
        this.executeVisualisation();
      },
      error => {
        console.log("error ", error);
      }
    );
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
      { def: 'POI_LOGISTIC', label: 'POI', show: this.POI.value },
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
    { def: 'POI_LOGISTIC', label: 'POI', show: this.POI.value },
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
