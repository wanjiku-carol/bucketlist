import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';



@Component({
    selector: 'app-users',
    templateUrl: './users.component.html',
    styleUrls: ['./users.component.css'],
    // providers: [UsersService]
})
export class UsersComponent  implements OnInit{
    username;
    email;
    password;
    public loggedIn = false;
    auth_token;
    message;
    public error;
    public resp: Object = {};

    constructor(private restangular: Restangular) {this.loggedIn = !!localStorage.getItem('auth_token') }

    registerUser(){
        let baseUrl = this.restangular.all('auth/register');
        let addAccount = baseUrl.post(
            { 'username':this.username,'email': this.email,'password':this.password }
        ).subscribe(resp => {
            console.log(this.resp=resp.message);
        }, err=>{this.error=err.data.message;
            console.log("There was an error logging in", err);
        })
    }
    loginUser(){
        let baseUrl = this.restangular.all('auth/login');
        let addAccount = baseUrl.post({'username':this.username, 'email':this.email,'password':this.password})
        .subscribe(resp => {
            console.log("login successful", resp);
            console.log(this.resp=resp.message)
            localStorage.setItem('auth_token', resp.auth_token);
            this.auth_token = resp.access_token;
            this.loggedIn = true;
        }, function(err) {
            console.log("There was an error logging in", err);
            console.log(this.error=err.data.message);
        });

    }

    isLoggedIn() {
        return this.loggedIn;
    }


    ngOnInit() {

    }

}
