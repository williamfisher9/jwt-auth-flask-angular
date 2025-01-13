import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

export const routes: Routes = [
    {path:'home', title: 'JWT AUTH - HOME', component: HomeComponent},
    {path:'login', title: 'JWT AUTH - LOGIN', component: LoginComponent },
    {path:'register', title: 'JWT AUTH - REGISTER', component: RegisterComponent},
    {path: '', redirectTo:'/home', pathMatch: 'full'},
    {path: '**', title: 'JWT AUTH - PAGE NOT FOUND', component: PageNotFoundComponent}
];
