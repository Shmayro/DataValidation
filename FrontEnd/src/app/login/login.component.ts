import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { LoginModel } from './login.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  error: any;
  loginForm: FormGroup;
  constructor(/*private authService: AuthService,*/
    private router: Router) { }

  ngOnInit(): void {
    this.loginForm=new FormGroup({
      username : new FormControl(''),
      password :new FormControl('')
    })
  }

  onSubmit(username: string, password: string) {
    /*this.authService.login(username, password).subscribe(
      success => this.router.navigate(['register']),
      error => this.error = error
    );*/
  }
}
