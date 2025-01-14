import { Component, input, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AppService } from '../services/app.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})

export class RegisterComponent{

  constructor(private appService : AppService, private router : Router){}

  emailAddress : string = 'hamza.hamdan@hotmail.com';
  firstName : string = 'Hamza';
  lastName : string = 'Hamdan';
  password : string = '12345678';

  responseError : string = '';

  handleRegisterRequest(){
    console.log(this.emailAddress, this.firstName, this.lastName, this.password);
    this.appService.sendRegisterRequest({emailAddress: this.emailAddress, 
                                        firstName: this.firstName, 
                                        lastName: this.lastName, 
                                        password: this.password, 
                                        roles: ['ADMIN_ROLE', 'USER_ROLE']})
    .subscribe({
      next: res => {
        if(res.status == 201){
          console.log(res)
          this.responseError = ''
          this.router.navigate(['/login'])
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
