import { Component, AfterContentInit, OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { Router } from '@angular/router';
import { RestangularModule, Restangular } from 'ngx-restangular';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',

})
export class AppComponent implements OnInit{
    public loggedIn = false;
    public reroute = false;
    public showHeader = true;
    public showLogin = false;
    public showRegister = false;
    public loginError;
    public registerError;
    login_password;
    login_email;
    auth_token;
    resp;
    reg_username;
    reg_email;
    reg_password;

    constructor( private restangular: Restangular, private router: Router ) {
        this.loggedIn = !!localStorage.getItem('auth_token')
    }
    loginUser(){
        let baseUrl = this.restangular.all('auth/login');
        let addAccount = baseUrl.post({'email':this.login_email,'password':this.login_password})
        .subscribe(resp => {
            localStorage.setItem('auth_token', resp.access_token);
            this.auth_token = resp.access_token;
            window.location.reload();
        }, err => {
            console.log(err.data.message)
            this.loginError = err.data.message;

        });
    }
    registerUser(){
        let baseUrl = this.restangular.all('auth/register/');
        let addAccount = baseUrl.post(
            { 'username': this.reg_username, 'email': this.reg_email, 'password':this.reg_password }
        ).subscribe(resp => {
            alert(this.resp=resp.message);
        }, err => {
            console.log(err.data.message)
            this.registerError = err.data.message;
        })
    }
    isLoggedIn() {
        return this.loggedIn;
    }

    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }

    displayLogin() {
        this.showHeader = false;
        this.showLogin = true;
    }

    displayRegister() {
        this.showHeader = false;
        this.showRegister = true;
    }



    ngOnInit() {
        if(window.location.pathname === '/' && this.isLoggedIn()) {
            this.router.navigate(['bucketlists']);
        }
    }

    title = 'app';
}
