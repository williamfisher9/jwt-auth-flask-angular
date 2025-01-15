import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppService } from '../services/app.service';
import { User } from '../interface/user';
import { UserProfileComponent } from "../user-profile/user-profile.component";

@Component({
  selector: 'app-user-home',
  standalone: true,
  imports: [UserProfileComponent],
  templateUrl: './user-home.component.html',
  styleUrl: './user-home.component.css'
})
export class UserHomeComponent implements OnInit{

  constructor(private route : ActivatedRoute, private appService : AppService){}

  user : User = null!;

  ngOnInit(): void {
    this.route.params.subscribe(res => {
      this.appService.getUserDetails(res['id']).subscribe(res => {
        console.log(res.message)
        this.user = res.message
      })
    });
  }

}
