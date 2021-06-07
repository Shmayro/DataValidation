import { HttpClient } from '@angular/common/http';
import { Component, Injectable, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiVerification {
  baseurl = "http://127.0.0.1:8000";

  constructor(private http: HttpClient) { }

  sendAddress(address): Observable<any> {
    const body = { addressU: address.AddressU, companyU: address.CompanyU };
    return this.http.get(this.baseurl + '/unitverif?Address=' + address.addressU + '&Company=' + address.companyU, { responseType: "json" });

  }
}

@Component({
  selector: 'app-unitverif',
  templateUrl: './unitverif.component.html',
  styleUrls: ['./unitverif.component.css'],
  providers: [ApiVerification],
})

export class UnitverifComponent {
  selectedAddress: any;

  companyINPUT: any;
  companyOUTPUT: any;
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
  ADDITIONALOUTPUT: any;

  showing:any;
  show: any;
  constructor(private DATACLEANING: ApiVerification) {
    this.selectedAddress = { addressU: '', companyU: '' };
    this.show = false;
    this.showing=false;
  }

  verify = () => {
    this.DATACLEANING.sendAddress(this.selectedAddress).subscribe(
      data => {
        this.showing=true
        // to choose witch data gonna be showing
        this.companyINPUT = data[0].companyINPUT
        this.AddressOUTPUT = data[0].AddressOUTPUT
        this.INBUILDINGOUTPUT=data[0].INBUILDINGOUTPUT
        this.EXTBUILDINGOUTPUT=data[0].EXTBUILDINGOUTPUT
        this.POILOGISTICOUTPUT=data[0].POILOGISTICOUTPUT
        this.ZONEOUTPUT=data[0].ZONEOUTPUT
        this.HouseNumOUTPUT=data[0].HouseNumOUTPUT
        this.RoadNameOUTPUT=data[0].RoadNameOUTPUT
        this.POBOXOUTPUT=data[0].POBOXOUTPUT
        this.zipcodeOUTPUT=data[0].zipcodeOUTPUT
        this.cityOUTPUT=data[0].cityOUTPUT
        this.countryOUTPUT=data[0].countryOUTPUT

        console.log(" test ", data[0])
      },
      error => {
        console.log("error ", error);
      }
    );
  }
}
