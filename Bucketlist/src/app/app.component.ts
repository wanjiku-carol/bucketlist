import { Component } from '@angular/core';
import { Http } from '@angular/http';
import { Restangular } from 'ngx-restangular';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    public loggedIn = false;
    auth_token;

    constructor(private http: Http, private restangular: Restangular) {
        this.loggedIn = !!localStorage.getItem('auth_token');
    }


    // post to login endpoint and get token
    // set token in localStorage
    loginUser () {

        let baseUrl = this.restangular.all('auth/login');

        let addAccount = baseUrl.post({'email':'shem@email.com','password':'shem_123'})
        .subscribe(resp => {
            console.log("login successful", resp);
            localStorage.setItem('auth_token', resp.auth_token);
            this.auth_token = resp.access_token;
            this.loggedIn = true;
        }, function(err) {
            console.log("There was an error logging in", err);
        });
    }

    isLoggedIn() {
        return this.loggedIn;
    }

    ngOnInit() {
        this.loginUser()

    }


    title = 'app';
}
