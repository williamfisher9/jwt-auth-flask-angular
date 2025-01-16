import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AppService } from '../services/app.service';
import { User } from '../interface/user';
import { UserProfileComponent } from "../user-profile/user-profile.component";
import { MenuComponent } from "../menu/menu.component";

@Component({
  selector: 'app-user-home',
  standalone: true,
  imports: [UserProfileComponent, MenuComponent],
  templateUrl: './user-home.component.html',
  styleUrl: './user-home.component.css'
})
export class UserHomeComponent implements OnInit{

  constructor(private route : ActivatedRoute, private appService : AppService, private router : Router){}

  user : User = null!;

  ngOnInit(): void {
    this.route.params.subscribe(res => {
      this.appService.getUserDetails(res['id']).subscribe(
        {
          next: (res) => {
            this.user = res.message
          },
          error: (err) => {
            this.router.navigate(['/login'])
          }
        }
      )
    });
  }

}
