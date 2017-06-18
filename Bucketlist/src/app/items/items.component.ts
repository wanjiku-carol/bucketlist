import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router } from '@angular/router';

@Component({
    selector: 'app-items',
    templateUrl: './items.component.html',
    styleUrls: ['./items.component.css']
})
export class ItemsComponent{

    constructor(private restangular: Restangular,private router: Router,) {
    }
    items;
    item;
    getItems(id){
        let baseUrl = this.restangular.one('bucketlists', id).all('items');
        let getItems = baseUrl.getList().subscribe(resp => {
            this.items = resp;
        });
    }
    

        ngOnInit() {
        }

    }
