import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { RouterModule, Routes } from '@angular/router';
import { Router } from '@angular/router';



@Component({
    selector: 'app-users',
    templateUrl: './users.component.html',
    styleUrls: ['./users.component.css'],
    // providers: [UsersService]
})
export class UsersComponent  implements OnInit{
    reg_username;
    reg_email;
    reg_password;
    login_password;
    login_email;
    auth_token;
    message;
    public error
    public resp: Object = {};

    constructor(private restangular: Restangular, private router: Router,) {
    }

    registerUser(){
        let baseUrl = this.restangular.all('auth/register');
        let addAccount = baseUrl.post(
            { 'username': this.reg_username, 'email': this.reg_email, 'password':this.reg_password }
        ).subscribe(resp => {
            console.log(this.resp=resp.message);
        }, function(err){console.log(this.error=err.data.message);
        })
    }
    ngOnInit() {

    }
    loginUser(){
        let baseUrl = this.restangular.all('auth/login');
        let addAccount = baseUrl.post({'email':this.login_email,'password':this.login_password})
        .subscribe(resp => {
            console.log("login successful", resp);
            console.log(this.resp=resp.message)
            localStorage.setItem('auth_token', resp.access_token);
            this.auth_token = resp.access_token;
            // this.loggedIn = true;
            // this.router.navigate(['/'])
            window.location.reload();
        }, function(err) {
            console.log(this.error=err.data.message);

        });
    }

}
