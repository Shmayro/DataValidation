import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ServicesService {
  api_link: string = "http://127.0.0.1:8000/"

  constructor(private http: HttpClient) { }

  getAllPosts() {
    this.http.get(this.api_link + "api/posts/")
  }
}
