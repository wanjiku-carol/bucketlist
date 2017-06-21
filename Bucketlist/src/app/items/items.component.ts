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
    getItems(bucketlist_id){
        let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).all('items');
        let getItems = baseUrl.getList().subscribe(resp => {
            this.items = resp;
        });
    }
    deleteItem(id){
        let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).one('items', id)
        let deleteItems = baseUrl.remove().subscribe(resp=>{
            console.log(resp)
            window.location.reload();
        });
    }
    addItems(){
        let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).all('items')
        let addItem = baseUrl.post({'name':this.name, 'done': this.done}).subscribe(resp => {
            this.getItems(this.bucketlist_id);
            this.name = '';
        });
        window.location.reload();
    }

    editItem(id){
        let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).one('item',id);
        let editItem = baseUrl.put({'name':this.name, 'done': this.done});
        window.location.reload();
    }

    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }


    ngOnInit() {
        this.route.params.subscribe(params => {
            this.bucketlist_id = +params['id'];
        })

        this.getItems(this.bucketlist_id);
    }

}
