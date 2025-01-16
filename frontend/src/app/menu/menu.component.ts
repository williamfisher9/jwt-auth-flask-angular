import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AppService } from '../services/app.service';
import { MenuItem } from '../interface/menu-item';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})

export class MenuComponent implements OnInit{

  constructor(private router : Router, private appService : AppService){}

  showLogo : boolean = false;
  path : string = '';

  menuItems : MenuItem[] = [];

  ngOnInit(): void {
    if(this.router.url == '/login' || this.router.url == '/register' || this.router.url == '/home'){
      this.showLogo = true
    } else {
      this.showLogo = false
    }

    this.appService.getMenuItems()
    .subscribe({
      next: res => {
        this.menuItems = res.message
      },
      error: err => {
        this.router.navigate(['/login'])
      }
    })
  }

  handleItemRoute(item : MenuItem){
    if(item.menu_item_name == 'home'){
      return `/users/${window.localStorage.getItem('user_id')}/home`
    } else {
      return ''
    }
  }

}
