import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { RegisterRequest } from '../interface/register-request';
import { LoginRequest } from '../interface/login-request';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private http : HttpClient) {}

  sendRegisterRequest(registerRequest : RegisterRequest) : Observable<any>{
    return this.http
    .post("http://localhost:8080/api/v1/users/register", {username: registerRequest.emailAddress, 
                                                                first_name: registerRequest.firstName, 
                                                                last_name: registerRequest.lastName, 
                                                                password: registerRequest.password,
                                                                roles: registerRequest.roles})
    .pipe(map(response => response));
  }

  sendLoginRequest(loginRequest : LoginRequest) : Observable<any>{
    return this.http.post("http://localhost:8080/api/v1/users/login", {username: loginRequest.username, password: loginRequest.password}).pipe(map(response => response));
  }
}

