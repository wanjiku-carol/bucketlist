import { Component, AfterContentInit, OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { Router } from '@angular/router';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
    public loggedIn = false;
    public reroute = false;

    constructor( private router: Router ) {
        this.loggedIn = !!localStorage.getItem('auth_token')
    }

    isLoggedIn() {
        return this.loggedIn;
    }

    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }

    ngOnInit() {
        if(window.location.pathname === '/' && this.isLoggedIn()) {
            this.router.navigate(['bucketlists']);
        }
    }

    title = 'app';
}
