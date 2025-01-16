import { Component, input, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AppService } from '../services/app.service';
import { MenuComponent } from "../menu/menu.component";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterLink, FormsModule, MenuComponent],
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

  isLoading : boolean = false;

  handleRegisterRequest(){
    this.isLoading = true;
    this.appService.sendRegisterRequest({emailAddress: this.emailAddress, 
                                        firstName: this.firstName, 
                                        lastName: this.lastName, 
                                        password: this.password, 
                                        roles: ['ADMIN_ROLE', 'USER_ROLE']})
    .subscribe({
      next: res => {
        if(res.status == 201){
          this.responseError = ''
          this.router.navigate(['/login'])
        }
      },
      error: err => {
        if (err.error.status != 201){
          this.responseError = err.error.message;
          this.isLoading = false;
        }
      },
      complete: () => {this.isLoading = false;}
    })
  }

  

  

}
