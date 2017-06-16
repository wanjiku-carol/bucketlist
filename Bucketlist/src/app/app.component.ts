import { Component, AfterContentInit, } from '@angular/core';
import { Http } from '@angular/http';
import { Restangular } from 'ngx-restangular';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent{
    public loggedIn = false;

    constructor() {
        this.loggedIn = !!localStorage.getItem('auth_token')
    }

    isLoggedIn() {
        return this.loggedIn;
    }

    title = 'app';
}
