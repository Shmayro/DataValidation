import { AfterViewInit, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit {
  data: any;
  constructor(private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.data = params['data'];
      console.log(this.data)
    });
  }
  ngOnInit(): void {
    if (this.data != null) {
      console.log(document.getElementById('IframeID'))
      //document.getElementById('IframeID').setAttribute("src", this.data);
    }
  }
  ngAfterViewInit() {

  }

}


