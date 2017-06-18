import { Component, AfterContentInit, } from '@angular/core';
import { Http } from '@angular/http';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent{
    public loggedIn = false;
    public reroute = false;

    constructor() {
        this.loggedIn = !!localStorage.getItem('auth_token')
    }

    isLoggedIn() {
        return this.loggedIn;
    }

    toItems(){
        this.reroute = true;
        // window.location.reload();
    }


    title = 'app';
}
