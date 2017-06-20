import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router , ActivatedRoute} from '@angular/router';

@Component({
    selector: 'app-items',
    templateUrl: './items.component.html',
    styleUrls: ['./items.component.css']
})
export class ItemsComponent{

    constructor(private restangular: Restangular, private route: ActivatedRoute,) {
    }
    items;
    bucketlist_id;
    name;
    done;
    getItems(id){
        let baseUrl = this.restangular.one('bucketlists', id).all('items');
        let getItems = baseUrl.getList().subscribe(resp => {
            this.items = resp;
        });
    }

    // getItem(bucketlist_id, id){
    //     let baseUrl = this.restangular.one('bucketlists', bucketlist_id).one('items', id);
    //     let getItem = baseUrl.get().subscribe(resp => {
    //         this.items = resp;
    //     });
    // }
    addItems(){
        let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).all('items')
        let addItem = baseUrl.post({'name':this.name, 'done': this.done}).subscribe(resp => {
            this.getItems(this.bucketlist_id);
            this.name = '';
        });
        window.location.reload();
    }


        ngOnInit() {
            this.route.params.subscribe(params => {
                this.bucketlist_id = +params['id'];
            })

            this.getItems(this.bucketlist_id);
            console.log(this.items)
            console.log("we're here", this.bucketlist_id)
        }

    }
