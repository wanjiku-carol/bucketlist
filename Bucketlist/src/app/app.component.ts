import { Component, AfterContentInit, } from '@angular/core';
import { Http } from '@angular/http';
import { Restangular } from 'ngx-restangular';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent{

    title = 'app';
}
