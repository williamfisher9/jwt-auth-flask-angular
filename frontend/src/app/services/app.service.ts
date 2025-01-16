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

  getUserDetails(id : number) : Observable<any> {
    return this.http.get(`http://localhost:8080/api/v1/users/${id}`, {headers: {'Authorization': `Bearer ${window.localStorage.getItem('token')}`}})
    .pipe(map(res => res))
  }

  updateProfileImage(id:number, file:File) : Observable<any>{
    const data = new FormData();
    data.append("id", id.toString());
    data.append("file", file, file.name);
    
    return this.http.post(`http://localhost:8080/api/v1/users/profile-image`, data, {headers: {'Authorization': `Bearer ${window.localStorage.getItem('token')}`}})
    .pipe(map(res => res))
  }
}

