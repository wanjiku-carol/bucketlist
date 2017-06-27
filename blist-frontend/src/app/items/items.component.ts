import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router , ActivatedRoute} from '@angular/router';
import * as moment from 'moment';

@Component({
  templateUrl: './items.component.html',
})
export class ItemsComponent implements OnInit {

  constructor(private restangular: Restangular, private route: ActivatedRoute,) { }
  items;
  bucketlist_id;
  current_bucketlist;
  name;
  done;
  edit = false;
  current_item;
  search_phrase;

  getItems(bucketlist_id){
      let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).all('items');
      let getItems = baseUrl.getList().subscribe(resp => {
          this.items = resp;
      });
  }
  deleteItem(id){
      let baseUrl = this.restangular.one('bucketlists', this.bucketlist_id).one('items', id)
      let deleteItems = baseUrl.remove().subscribe(resp=>{
        //   console.log(resp)
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
      this.edit = true;
      this.current_item = this.restangular.one('bucketlists', this.bucketlist_id).one('items', id);
      this.current_item.get().subscribe(resp => {
          this.name = resp.name;
          this.done = resp.done;
      });
  }
  saveItem(){
      this.current_item.name = this.name
      this.current_item.done = this.done
      let editItems = this.current_item.put().subscribe(resp => {
          console.log(resp);
          this.name = '';
          this.edit = false;
          this.getItems(this.bucketlist_id);
      }, function(err) {
          console.log(err)

      });;
  }

  cancel() {
      this.name = '';
      this.edit = false;
  }

  getCurrentBucketlist() {
      this.restangular.one('bucketlists', this.bucketlist_id).get().subscribe(resp => {
          this.current_bucketlist = resp.name;
      });
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
      this.getCurrentBucketlist();
  }

}
