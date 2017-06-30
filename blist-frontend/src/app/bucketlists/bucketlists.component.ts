import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router } from '@angular/router';

@Component({
  templateUrl: './bucketlists.component.html',
})
export class BucketlistsComponent implements OnInit {

  constructor(private restangular: Restangular,private router: Router,) { }
  bucketlists;
  current_bucketlist;
  name;
  search_phrase;
  edit = false;

  getBuckelists(){
      let baseUrl = this.restangular.all('bucketlists');
      baseUrl.getList().subscribe(resp => {
          this.bucketlists = resp;
      });
  }
  deleteBucketlist(id){
      let baseUrl = this.restangular.one('bucketlists', id);
      let deleteBucketlists = baseUrl.remove().subscribe(resp=>{
          console.log(resp)
          window.location.reload();
      });
  }
  addBucketlist(){
      let baseUrl = this.restangular.all('bucketlists');
      let addBucketlists = baseUrl.post({'name':this.name}).subscribe(resp => {
          this.getBuckelists();
          this.name = '';
      });
  }
  editBucketlist(id){
      this.edit = true;
      this.current_bucketlist = this.restangular.one('bucketlists', id);
      this.current_bucketlist.get().subscribe(resp => {
          this.name = resp.name;
      });
  }
  saveBucketlist(){
      this.current_bucketlist.name = this.name
      let editBucketlists = this.current_bucketlist.put().subscribe(resp => {
          this.getBuckelists();
          this.name = '';
          this.edit = false;
      }, function(err) {

      });;
  }

  searchBucketlist(){
      this.restangular.all("bucketlists").customGET('', { q: this.search_phrase}).subscribe(resp => {
          this.bucketlists = resp;
      });
  }

  cancel() {
      this.name = '';
      this.edit = false;
  }

  logout() {
      localStorage.removeItem('auth_token');
      window.location.reload();
  }


  ngOnInit() {
      this.getBuckelists();
  }

}
