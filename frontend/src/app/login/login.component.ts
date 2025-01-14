import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { AppService } from '../services/app.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  constructor(private appService : AppService, private router : Router){}

  username : string = 'hamza.hamdan@hotmail.com'
  password : string = '12345678'

  responseError : string = ''

  handleLoginRequest(){
    this.appService.sendLoginRequest({username: this.username, password : this.password})
    .subscribe({
      next: res => {
        if(res.status == 200){
          console.log(res)
          this.responseError = ''
        }
      },
      error: err => {
        if (err.error.status != 201){
          console.log(err.error)
          this.responseError = err.error.message
        }
      }
    })
  }
}
