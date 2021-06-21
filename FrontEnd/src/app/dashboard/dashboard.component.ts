import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent {
  data: any;
  url:string;
  constructor(private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.data = params['data'];
      console.log(this.data)
      this.url='./assets/profiling.html';

    });
  }
  ngOnInit(): void {
    if (this.data != null) {
      //console.log(document.getElementById('IframeID'))
      //var iframe = document.getElementById('IframeID');
      //console.log(iframe);
      ////document.getElementById('IframeID').setAttribute("src", this.data);
    }
  }

}


