// pos_orders_all js
odoo.define('pos_orders_all.pos', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    
    var utils = require('web.utils');
    var round_pr = utils.round_precision;

    var _t = core._t;




	models.load_models({
        model: 'stock.location',
        fields: [],
        //ids:    function(self){ return [self.config.stock_location_id[0]]; },

        loaded: function(self, locations){
            var i;
            self.locations = locations[0];
            
    	    if (self.config.show_stock_location == 'specific')
    	    {

		        // associate the Locations with their quants.
		        var ilen = locations.length;
		        for(i = 0; i < ilen; i++){
		            if(locations[i].id === self.config.stock_location_id[0]){
					    var ayaz = locations[i];
					    self.locations = ayaz;
					    //console.log("ayazzzzzzzzzzzzzzzzzzzzzzzzzzzz callleddddddddddddddddddddd",ayaz, self.config.stock_location_id[0]);
		            }
		        }
            }

        },
	});
	
	
    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var product_model = _.find(this.models, function(model){ return model.model === 'product.product'; });
            product_model.fields.push('qty_available','incoming_qty','outgoing_qty','type');

            return _super_posmodel.initialize.call(this, session, attributes);
        },
        
        push_order: function(order, opts){
            var self = this;
            var pushed = _super_posmodel.push_order.call(this, order, opts);
            var client = order && order.get_client();
            
            if (order){
                if (this.config.pos_display_stock === true && this.config.pos_stock_type == 'onhand' || this.config.pos_stock_type == 'available')
                {
		            order.orderlines.each(function(line){
		               var qty = line.quantity;
		               var qty_available = line.product.qty_available;
		               var ayaz = line.product.qty_available - line.quantity;
		               qty_available = ayaz;
		               
		               var product = self.db.get_product_by_id(line.product.id);
		               var all = $('.product');
						$.each(all, function(index, value) {
							var product_id = $(value).data('product-id');
							if (product_id == product.id)
							{
								$(value).find('#stockqty').html(qty_available);
							}
						});
		        
		            });
		        }
            }
            return pushed;
        }
    });
    


    screens.ProductScreenWidget.include({
        show: function() {
            var self = this;
            this._super();
            
    	    if (self.pos.config.show_stock_location == 'specific')
    	    {
			    var partner_id = this.pos.get_client();
		    	var location = self.pos.locations;


                rpc.query({
				        model: 'stock.quant',
				        method: 'get_stock_location_qty',
				        args: [partner_id ? partner_id.id : 0, location],
		            
		            }).then(function(output) {
		            	
				       var all = $('.product');
						$.each(all, function(index, value) {
							var product_id = $(value).data('product-id');
						
							for (var i = 0; i < output.length; i++) {
								var product = output[i][product_id];
								$(value).find('#stockqty').html(product);
							}
						});
		        });
            
            }
            
        },
    }); 
    
    screens.ProductScreenWidget.include({ 
    
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
        },
    
    });   
    
    screens.ProductListWidget.include({
		init: function(parent, options) {
		    var self = this;
		    this._super(parent,options);
		    this.model = options.model;
		    this.productwidgets = [];
		    this.weight = options.weight || 0;
		    this.show_scale = options.show_scale || false;
		    this.next_screen = options.next_screen || false;

		    this.click_product_handler = function(){
		        var product = self.pos.db.get_product_by_id(this.dataset.productId);
		        //console.log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~product",self.pos.config)
		        
		        if (product.type == 'product')
		        {
				    // Deny POS Order When Product is Out of Stock
				    if (product.qty_available <= self.pos.config.pos_deny_order)
				    {
				    	self.gui.show_popup('error',{
							'title': _t('Deny Order'),
				            'body': _t("Deny Order." + "(" + product.display_name + ")" + " is Out of Stock.")
				        });
				    }
				     
				    
				    
				    // Allow POS Order When Product is Out of Stock
				    else if (product.qty_available <= 0 && self.pos.config.pos_allow_order == false)
				    {
						self.gui.show_popup('error',{
							'title': _t('Error: Out of Stock'),
							'body': _t("(" + product.display_name + ")" + " is Out of Stock."),
						});
				    } else {
				    	options.click_product_action(product);
				    }
		        } else {
				    	options.click_product_action(product);
				    }
		        
		        
		        
		    };

		},
   
	});
    // End ProductListWidget start


    // Popup start

    var ValidQtyPopupWidget = popups.extend({
        template: 'ValidQtyPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        //
        show: function(options) {
            var self = this;
            this._super(options);
        },
        //
        renderElement: function() {
            var self = this;
            this._super();
            this.$('#back_to_products').click(function() {
            	self.gui.show_screen('products');
			});            	
        },

    });
    gui.define_popup({
        name: 'valid_qty_popup_widget',
        widget: ValidQtyPopupWidget
    });

    // End Popup start
    
    // ActionpadWidget start
    screens.ActionpadWidget.include({
		renderElement: function() {
		    var self = this;
		    this._super();
		    this.$('.pay').click(function(){
		        var order = self.pos.get_order();

		        var has_valid_product_lot = _.every(order.orderlines.models, function(line){
		            return line.has_valid_product_lot();
		        });
		        if(!has_valid_product_lot){
		            self.gui.show_popup('error',{
		                'title': _t('Empty Serial/Lot Number'),
		                'body':  _t('One or more product(s) required serial/lot number.'),
		                confirm: function(){
		                    self.gui.show_screen('payment');
		                },
		            });
		        }else{
		            self.gui.show_screen('payment');
		        }



    	    if (self.pos.config.show_stock_location == 'specific')
    	    {
			    var partner_id = self.pos.get_client();
		    	var location = self.pos.locations;
		    	//console.log("ppppppppppppppppppppppppppppppppppppppllllllllllllllllllllllllllll",partner_id, location);


                rpc.query({
				        model: 'stock.quant',
				        method: 'get_stock_location_qty',
				        args: [partner_id ? partner_id.id : 0, location],
		            
		            }).then(function(output) {
		               //console.log("outputttttttttttttttttttttttttttttttttttttttttttt",output);	


						var lines = order.get_orderlines();

						for (var i = 0; i < lines.length; i++) {
						
		                    for (var j = 0; j < output.length; j++) {
		                    
		                    var values = $.map(output[0], function(value, key) { 

								var keys = $.map(output[0], function(value, key) {
									//console.log("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",key,value);

									if (lines[i].product.type == 'product'){
										if (lines[i].product['id'] == key){
											if (lines[i].quantity <= value) {
												//console.log( "ifffffffffffffffffffffffffffffffffffff");
												self.gui.show_screen('payment');
											}else { //(line1.quantity > line1.product['qty_available']){
												//console.log( "elseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
												self.gui.show_popup('valid_qty_popup_widget', {});
											}
										}
									}
								
								
								});
									                    	
		                    });
								
		                    }
						}
						                        
                                		               
		        });
            
            } else {
            
            
				// When Ordered Qty it More than Available Qty, Raise Error popup

				var lines = order.get_orderlines();

				for (var i = 0; i < lines.length; i++) {
				    
				    //console.log("pppppppppppppppppppppppppppppppppppppproduct",lines[i].quantity, lines[i].product['qty_available'], lines[i]);
				    
				    if (lines[i].product.type == 'product'){
						if (lines[i].quantity <= lines[i].product['qty_available']) {
						    self.gui.show_screen('payment');
						}else { //(line1.quantity > line1.product['qty_available']){
			                self.gui.show_popup('valid_qty_popup_widget', {});
						}
			    	}
				}
				
				/*
				var has_valid_qty = _.every(order.orderlines.models, function(line1){
					console.log("pppppppppppppppppppppppppppppppppppppproduct",line1.quantity, line1.product['qty_available']);
					if (line1.quantity <= line1.product['qty_available']){
						self.gui.show_screen('payment');
					}else { //(line1.quantity > line1.product['qty_available']){
                        self.gui.show_popup('valid_qty_popup_widget', {});
		        }
	
				});
				*/
			}	
						        
		    });
		    this.$('.set-customer').click(function(){
		        self.gui.show_screen('clientlist');
		    });
            
        },
    });  
    // End ActionpadWidget start
            
        
    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        //Cantidad en letras
        numletras: function(n){
             var o=new Array("Diez", "Once", "Doce", "Trece", "Catorce", "Quince", "Dieciseis", "Diecisiete", "Dieciocho", "Diecinueve", "Veinte", "Veintiuno", "Veintidos", "Veintitres", "Veinticuatro", "Veinticinco", "Veintiseis", "Veintisiete", "Veintiocho", "Veintinueve");
             var u=new Array("Cero", "Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve");
             var d=new Array("", "", "", "Treinta", "Cuarenta", "Cincuenta", "Sesenta", "Setenta", "Ochenta", "Noventa");
             var c=new Array("", "Ciento", "Doscientos", "Trescientos", "Cuatrocientos", "Quinientos", "Seiscientos", "Setecientos", "Ochocientos", "Novecientos");

             var n=parseFloat(n).toFixed(2); /*se limita a dos decimales, no sabía que existía toFixed() :)*/
             var p=n.toString().substring(n.toString().indexOf(".")+1); /*decimales*/
             var m=n.toString().substring(0,n.toString().indexOf(".")); /*número sin decimales*/
             var m=parseFloat(m).toString().split("").reverse(); /*tampoco que reverse() existía :D*/
             var t="";

             for (var i=0; i<m.length; i+=3){
                var x=t;
                var b=m[i+1]!=undefined?parseFloat(m[i+1].toString()+m[i].toString()):parseFloat(m[i].toString());
                t=m[i+2]!=undefined?(c[m[i+2]]+" "):"";
                t+=b<10?u[b]:(b<30?o[b-10]:(d[m[i+1]]+(m[i]=='0'?"":(" y "+u[m[i]]))));
                t=t=="Ciento Cero"?"Cien":t;
                if (2<i&&i<6)
                  t=t=="Uno"?"Mil ":(t.replace("Uno","Un")+" Mil ");
                if (5<i&&i<9)
                  t=t=="Uno"?"Un Millón ":(t.replace("Uno","Un")+" Millones ");
                t+=x;
              }

             t+=" Pesos "+p+"/100 M.N";
             /*correcciones*/
             t=t.replace("  "," ");
             t=t.replace(" Cero","");
             return t;
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.coupon_id = this.coupon_id;
            return json;
        },
        
        
        // Total Items Count in exports.Orderline = Backbone.Model.extend ...
	    get_total_items: function() {
           var utils = require('web.utils');
           var round_pr = utils.round_precision;
            
             return round_pr(this.orderlines.reduce((function(sum, orderLine) {
            return sum + orderLine.quantity;

        }), 0), this.pos.currency.rounding);
    sum
        },
        
        get_fixed_discount: function() {
		    return round_pr(this.orderlines.reduce((function(sum, orderLine) {
		        return sum + (orderLine.get_discount());
		    }), 0), this.pos.currency.rounding);
		},
		
		//default pos multi pricelist features in v11.. so when change pricelist den stock quantity will display correctly.. 
		set_pricelist: function (pricelist) {
            var self = this;
            this.pricelist = pricelist;
            _.each(this.get_orderlines(), function (line) {
                line.set_unit_price(line.product.get_price(self.pricelist, line.get_quantity()));
                self.fix_tax_included_price(line);
            });


                if (self.pos.config.show_stock_location == 'specific')
                {
                    var partner_id = this.pos.get_client();
                    var location = self.pos.locations;


                    rpc.query({
                            model: 'stock.quant',
                            method: 'get_stock_location_qty',
                            args: [partner_id ? partner_id.id : 0, location],
                        
                        }).then(function(output) {
                            
                           var all = $('.product');
                            $.each(all, function(index, value) {
                                var product_id = $(value).data('product-id');
                            
                                for (var i = 0; i < output.length; i++) {
                                    var product = output[i][product_id];
                                    $(value).find('#stockqty').html(product);
                                }
                            });
                    });
                
                }

            this.trigger('change');
        },
    
    
    
    });
    
    
    
// Load Models here...

    models.load_models({
        model: 'pos.order',
        fields: ['name', 'id', 'date_order', 'partner_id', 'pos_reference', 'lines', 'amount_total', 'session_id', 'state', 'company_id','coupon_id'],
        domain: function(self){ return [['session_id', '=', self.pos_session.name],['state', 'not in', ['draft', 'cancel']]]; },
        loaded: function(self, orders){
        	self.db.all_orders_list = orders;

        	self.db.get_orders_by_id = {};
            orders.forEach(function(order) {
                self.db.get_orders_by_id[order.id] = order;
            });
            self.orders = orders;
        },
    });
    
    models.load_models({
        model: 'pos.gift.coupon',
        fields: ['name', 'gift_coupen_code', 'user_id', 'issue_date', 'expiry_date', 'validity', 'total_available', 'partner_id', 'order_ids', 'active', 'amount', 'description','used','coupon_count', 'coupon_apply_times','expiry_date','partner_true','partner_id'],
        domain: null,
        loaded: function(self, pos_gift_coupon) { 
            self.pos_gift_coupon = pos_gift_coupon;    
        },
    });
    
    models.load_models({
        model: 'pos.coupons.setting',
        fields: ['name', 'product_id', 'min_coupan_value', 'max_coupan_value', 'max_exp_date', 'one_time_use', 'partially_use', 'default_name', 'default_validity', 'default_value', 'default_availability', 'active'],
        domain: null,
        loaded: function(self, pos_coupons_setting) { 
            self.pos_coupons_setting = pos_coupons_setting;
        },
    });

    models.load_models({
        model: 'pos.order.line',
        fields: ['order_id', 'product_id', 'discount', 'qty', 'price_unit',],
        domain: function(self) {
            var order_lines = []
            var orders = self.db.all_orders_list;
            for (var i = 0; i < orders.length; i++) {
                order_lines = order_lines.concat(orders[i]['lines']);
            }
            return [
                ['id', 'in', order_lines]
            ];
        },
        loaded: function(self, pos_order_line) {
            self.db.all_orders_line_list = pos_order_line;
            self.db.get_lines_by_id = {};
            pos_order_line.forEach(function(line) {
                self.db.get_lines_by_id[line.id] = line;
            });

            self.pos_order_line = pos_order_line;
        },
    });


// bi_pos_custom_discount load models
    models.load_models({
        model: 'pos.custom.discount',
        fields: ['name','discount','description','available_pos_ids'],
        domain: function(self) {
            return [
                ['id', 'in', self.config.custom_discount_ids]
            ];
        },
        loaded: function(self, pos_custom_discount) {
            
            self.pos_custom_discount = pos_custom_discount;
        },

    });
    
    models.load_models({
        model: 'pos.config',
        fields: ['allow_custom_discount','custom_discount_ids'],
        domain: null,
        loaded: function(self, pos_custom_config) {
            
            self.pos_custom_config = pos_custom_config;
        },

    });
    
    // exports.Orderline = Backbone.Model.extend ...
    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
    
		get_all_prices: function(){
		    
		    if (this.pos.config.discount_type == 'percentage')
		    {
				var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
				//console.log("ifffffffffff priceeeeeeeeeeeeeeeeeeeeeeeeeeee unitttt",price_unit);
			}
			else if (this.pos.config.discount_type == 'fixed')
			{
				var price_unit = this.get_unit_price() - this.get_discount();
				//console.log("elseeeeeeeeeee priceeeeeeeeeeeeeeeeeeeeeeeeeeee unitttt",price_unit);			
			}	
		    var taxtotal = 0;

		    var product =  this.get_product();
		    var taxes_ids = product.taxes_id;
		    var taxes =  this.pos.taxes;
		    var taxdetail = {};
		    var product_taxes = [];

		    _(taxes_ids).each(function(el){
		        product_taxes.push(_.detect(taxes, function(t){
		            return t.id === el;
		        }));
		    });

		    var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
		    _(all_taxes.taxes).each(function(tax) {
		        taxtotal += tax.amount;
		        taxdetail[tax.id] = tax.amount;
		    });

		    return {
		        "priceWithTax": all_taxes.total_included,
		        "priceWithoutTax": all_taxes.total_excluded,
		        "tax": taxtotal,
		        "taxDetails": taxdetail,
		    };
		},
		
    });
    // End Orderline start

        

	 // ReceiptScreenWidgetNew start
	 var ReceiptScreenWidgetNew = screens.ScreenWidget.extend({
       template: 'ReceiptScreenWidgetNew',
        show: function() {
            var self = this;
            self._super();
            $('.button.back').on("click", function() {
                self.gui.show_screen('see_all_orders_screen_widget');
            });
            $('.button.print').click(function() {
                var test = self.chrome.screens.receipt;
                setTimeout(function() { self.chrome.screens.receipt.lock_screen(false); }, 1000);
                if (!test['_locked']) {
                    self.chrome.screens.receipt.print_web();
                    self.chrome.screens.receipt.lock_screen(true);
                }
            });
        }
    });
    gui.define_screen({ name: 'ReceiptScreenWidgetNew', widget: ReceiptScreenWidgetNew });


    // SeeAllOrdersScreenWidget start

    var SeeAllOrdersScreenWidget = screens.ScreenWidget.extend({
        template: 'SeeAllOrdersScreenWidget',
        init: function(parent, options) {
            this._super(parent, options);
            //this.options = {};
        },
        //

        line_selects: function(event,$line,id){
        	//console.log('calllllllll',id);
        	var self = this;
            var orders = this.pos.db.get_orders_by_id[id];
            this.$('.client-list .lowlight').removeClass('lowlight');
            if ( $line.hasClass('highlight') ){
                $line.removeClass('highlight');
                $line.addClass('lowlight');
                this.display_orders_detail('hide',orders);
                this.new_clients = null;
                //this.toggle_save_button();
            }else{
                this.$('.client-list .highlight').removeClass('highlight');
                $line.addClass('highlight');
                var y = event.pageY - $line.parent().offset().top;
                this.display_orders_detail('show',orders,y);
                this.new_clients = orders;
                //this.toggle_save_button();
            }

        },

        display_orders_detail: function(visibility,order,clickpos){
            var self = this;
            var contents = this.$('.client-details-contents');
            var parent   = this.$('.orders-line ').parent();
            var scroll   = parent.scrollTop();
            var height   = contents.height();

            contents.off('click','.button.edit');
            contents.off('click','.button.save');
            contents.off('click','.button.undo');

            this.editing_client = false;
            this.uploaded_picture = null;

            if(visibility === 'show'){
                contents.empty();
                contents.append($(QWeb.render('OrderDetails',{widget:this,order:order})));

                var new_height   = contents.height();

                if(!this.details_visible){
                    if(clickpos < scroll + new_height + 20 ){
                        parent.scrollTop( clickpos - 20 );
                    }else{
                        parent.scrollTop(parent.scrollTop() + new_height);
                    }
                }else{
                    parent.scrollTop(parent.scrollTop() - height + new_height);
                }

                this.details_visible = true;
                //this.toggle_save_button();
            } else if (visibility === 'hide') {
                contents.empty();
                if( height > scroll ){
                    contents.css({height:height+'px'});
                    contents.animate({height:0},400,function(){
                        contents.css({height:''});
                    });
                }else{
                    parent.scrollTop( parent.scrollTop() - height);
                }
                this.details_visible = false;
                //this.toggle_save_button();
            }
        },

        get_selected_partner: function() {
            var self = this;
            if (self.gui)
                return self.gui.get_current_screen_param('selected_partner_id');
            else
                return undefined;
        },

         render_list_orders: function(orders, search_input){
            var self = this;
            var selected_partner_id = this.get_selected_partner();
            var selected_client_orders = [];
            if (selected_partner_id != undefined) {
                for (var i = 0; i < orders.length; i++) {
                    if (orders[i].partner_id[0] == selected_partner_id)
                        selected_client_orders = selected_client_orders.concat(orders[i]);
                }
                orders = selected_client_orders;
            }
            
            if (search_input != undefined && search_input != '') {
                var selected_search_orders = [];
                var search_text = search_input.toLowerCase()
                //console.log("111111111111111111111111query",search_text)
                for (var i = 0; i < orders.length; i++) {
                    if (orders[i].partner_id == '') {
                        orders[i].partner_id = [0, '-'];
                    }
                    //console.log("111111111111111111111111query",search_text
                    if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].pos_reference.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1)) {
                        selected_search_orders = selected_search_orders.concat(orders[i]);
                        //console.log("1111111111111111111111111111new_order_data ",new_order_data)
                    }
                }
                orders = selected_search_orders;
                //console.log("upar orderssssssssssssssssssssssssssssss",orders)
            }
            

            var content = this.$el[0].querySelector('.orders-list-contents');
            content.innerHTML = "";
            for(var i = 0, len = Math.min(orders.length,1000); i < len; i++){
                var order    = orders[i];
                var ordersline_html = QWeb.render('OrdersLine',{widget: this, order:orders[i], selected_partner_id: orders[i].partner_id[0]});
                var ordersline = document.createElement('tbody');
                ordersline.innerHTML = ordersline_html;
                ordersline = ordersline.childNodes[1];
                content.appendChild(ordersline);

            }
        },
        //
        show: function(options) {
            var self = this;
            this._super(options);

            this.details_visible = false;

            var orders = self.pos.db.all_orders_list;
            this.render_list_orders(orders, undefined);

	    	this.$('.back').click(function(){
		        //self.gui.back();
		        self.gui.show_screen('products');
            });
            
            //this code is for Search Orders
            this.$('.search-order input').keyup(function() {
                //console.log("***************************************ordersssssssssssssss",this.value)
                self.render_list_orders(orders, this.value);
            });
            
            //Return Order
            this.$('.orders-list-contents').delegate('.return-order', 'click', function(result) {
                var order_id = parseInt(this.id);
                var selectedOrder = null;
		        for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
		            if (orders[i] && orders[i].id == order_id) {
		                selectedOrder = orders[i];
		            }
		        }
		        
                var orderlines = [];
            	var order_list = self.pos.db.all_orders_list;
                var order_line_data = self.pos.db.all_orders_line_list;

                selectedOrder.lines.forEach(function(line_id) {
		            var line = self.pos.db.get_lines_by_id[line_id];
		            var product = self.pos.db.get_product_by_id(line.product_id[0]);
		            orderlines.push(line);
                });

            	self.gui.show_popup('pos_return_order_popup_widget', { 'orderlines': orderlines, 'order': selectedOrder });
            });
            //End Return Order
            
            

            //Re-Order
            this.$('.orders-list-contents').delegate('.re-order', 'click', function(result) {
                
                var order_id = parseInt(this.id);
                
                var selectedOrder = null;
		        for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
		            if (orders[i] && orders[i].id == order_id) {
		                selectedOrder = orders[i];
		            }
		        }
		        
                var orderlines = [];
            	var order_list = self.pos.db.all_orders_list;
                var order_line_data = self.pos.db.all_orders_line_list;

                selectedOrder.lines.forEach(function(line_id) {
		            var line = self.pos.db.get_lines_by_id[line_id];
		            var product = self.pos.db.get_product_by_id(line.product_id[0]);
		            orderlines.push(line);
                });

            	self.gui.show_popup('pos_re_order_popup_widget', { 'orderlines': orderlines, 'order': selectedOrder });
            });
            //End Re-Order
            
            //Receipt Reprint
            this.$('.orders-list-contents').delegate('.print-order', 'click', function(result) {
                //console.log("clikckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkked")
                var order_id = parseInt(this.id);
                var orderlines = [];
		        var paymentlines = [];
		        var discount = 0;

                var selectedOrder = null;
		        for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
		            if (orders[i] && orders[i].id == order_id) {
		                selectedOrder = orders[i];
		                //console.log("selectedOrder_newewwwwwwwwwwwwwwwwwwwwwwwwwwwww",selectedOrder)
		            }
		        }

                rpc.query({
				        model: 'pos.order',
				        method: 'print_pos_receipt',
				        args: [order_id],
		            
		            }).then(function(output) {
		            

                    //console.log("outputttttttttttttttttttttt", output)

					orderlines = output[0];
		            paymentlines = output[2];
		            discount = output[1];
		            self.gui.show_screen('ReceiptScreenWidgetNew');
		            $('.pos-receipt-container').html(QWeb.render('PosTicket1',{
		                widget:self,
		                order: selectedOrder,
		                paymentlines: paymentlines,
		                orderlines: orderlines,
		                discount_total: discount,
		                change: output[3],
		            }));


				});
				//End Receipt Reprint


            var contents = self.$('.orders-list-contents');
            contents.empty();
            var parent = self.$('.client-list').parent();
            parent.scrollTop(0);

        });

        },
        //


    });
    gui.define_screen({
        name: 'see_all_orders_screen_widget',
        widget: SeeAllOrdersScreenWidget
    });

    // End SeeAllOrdersScreenWidget



    // PosReOrderPopupWidget Popup start

    var PosReOrderPopupWidget = popups.extend({
        template: 'PosReOrderPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        //
        show: function(options) {
        	options = options || {};
            var self = this;
            this._super(options);
            this.orderlines = options.orderlines || [];

        },
        //
        renderElement: function() {
            var self = this;
            this._super();
            var selectedOrder = this.pos.get_order();
            var orderlines = self.options.orderlines;
            var order = self.options.order;

			var reorder_products = {};

            this.$('#apply_reorder').click(function() {
                var entered_code = $("#entered_item_qty").val();
                var list_of_qty = $('.entered_item_qty');

				$.each(list_of_qty, function(index, value) {
				 	var entered_item_qty = $(value).find('input');
               	    var qty_id = parseFloat(entered_item_qty.attr('qty-id'));
		            var line_id = parseFloat(entered_item_qty.attr('line-id'));
		            var entered_qty = parseFloat(entered_item_qty.val());

		            reorder_products[line_id] = entered_qty;
            	});
            	//return reorder_products;


            	Object.keys(reorder_products).forEach(function(line_id) {
            		var line = self.pos.db.get_lines_by_id[line_id];
                	var product = self.pos.db.get_product_by_id(line.product_id[0]);
                	selectedOrder.add_product(product, {
                        quantity: parseFloat(reorder_products[line_id]),
                        price: line.price_unit,
                        discount: line.discount
                    });
                    selectedOrder.selected_orderline.original_line_id = line.id;
            	});
            	self.pos.set_order(selectedOrder);
            	self.gui.show_screen('products');

               });


        },

    });
    gui.define_popup({
        name: 'pos_re_order_popup_widget',
        widget: PosReOrderPopupWidget
    });

    // End PosReOrderPopupWidget Popup start



    // PosReturnOrderPopupWidget Popup start

    var PosReturnOrderPopupWidget = popups.extend({
        template: 'PosReturnOrderPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        //
        show: function(options) {
        	options = options || {};
            var self = this;
            this._super(options);
            this.orderlines = options.orderlines || [];

        },
        //
        renderElement: function() {
            var self = this;
            this._super();
            var selectedOrder = this.pos.get_order();
            var orderlines = self.options.orderlines;
            var order = self.options.order;

			var return_products = {};
			var exact_return_qty = {};
            		var exact_entered_qty = {};



            this.$('#apply_return_order').click(function() {
                var entered_code = $("#entered_item_qty").val();
                var list_of_qty = $('.entered_item_qty');


				$.each(list_of_qty, function(index, value) {
				 	var entered_item_qty = $(value).find('input');
               	    var qty_id = parseFloat(entered_item_qty.attr('qty-id'));
		            var line_id = parseFloat(entered_item_qty.attr('line-id'));
		            var entered_qty = parseFloat(entered_item_qty.val());
		            
		            exact_return_qty = qty_id;
                    	    exact_entered_qty = entered_qty || 0;

		            if(!exact_entered_qty){
		            	return;
                    }
                    else if (exact_return_qty >= exact_entered_qty){
		              return_products[line_id] = entered_qty;
                    }
                    else{
                    alert("Cannot Return More quantity than purchased")
                    }

            	});
            	//return return_products;


            	Object.keys(return_products).forEach(function(line_id) {
            		var line = self.pos.db.get_lines_by_id[line_id];
                	var product = self.pos.db.get_product_by_id(line.product_id[0]);
                	
                	selectedOrder.add_product(product, {
                        quantity: parseFloat(return_products[line_id]),
                        price: - line.price_unit,
                        discount: line.discount
                    });
                    selectedOrder.selected_orderline.original_line_id = line.id;
            	});
            	self.pos.set_order(selectedOrder);
            	self.gui.show_screen('products');

               });

        },

    });
    gui.define_popup({
        name: 'pos_return_order_popup_widget',
        widget: PosReturnOrderPopupWidget
    });

    // End PosReturnOrderPopupWidget Popup start





	// Start SeeAllOrdersButtonWidget

    var SeeAllOrdersButtonWidget = screens.ActionButtonWidget.extend({
        template: 'SeeAllOrdersButtonWidget',

        button_click: function() {
            var self = this;
            this.gui.show_screen('see_all_orders_screen_widget', {});
        },

    });

    screens.define_action_button({
        'name': 'See All Orders Button Widget',
        'widget': SeeAllOrdersButtonWidget,
        'condition': function() {
            return true;
        },
    });
    // End SeeAllOrdersButtonWidget

// Start ClientListScreenWidget
		gui.Gui.prototype.screen_classes.filter(function(el) { return el.name == 'clientlist'})[0].widget.include({
            show: function(){
		        this._super();
		        var self = this;
		        this.$('.view-orders').click(function(){
            		self.gui.show_screen('see_all_orders_screen_widget', {});
            	});


            $('.selected-client-orders').on("click", function() {
                self.gui.show_screen('see_all_orders_screen_widget', {
                    'selected_partner_id': this.id
                });
            });

        },
    });


	// Start CreateSalesOrderButtonWidget
	
    var CreateSalesOrderButtonWidget = screens.ActionButtonWidget.extend({
        template: 'CreateSalesOrderButtonWidget',
        
        renderElement: function(){
		    var self = this;
		    this._super();
          
          //this.$('#create_sales_order').click(function() {
          this.$el.click(function(){
                
		        var order = self.pos.get('selectedOrder');
		        console.log("selewcted orderrrrrrrrrrrrrr",order)

                var partner_id = false
                if (order.get_client() != null)
                    partner_id = order.get_client();
                
                 // Popup Occurs when no Customer is selected...
                    if (!partner_id) {
                        self.gui.show_popup('error', {
                            'title': _t('Unknown customer'),
                            'body': _t('You cannot Create Sales Order. Select customer first.'),
                        });
                        return;
                    }

		        var orderlines = order.orderlines;
		        
		        
		        // Popup Occurs when not a single product in orderline...
                    if (orderlines.length === 0) {
                        self.gui.show_popup('error', {
                            'title': _t('Empty Order'),
                            'body': _t('There must be at least one product in your order before Create Sales Order.'),
                        });
                        return;
                    }
		        
		        var pos_product_list = [];
				for (var i = 0; i < orderlines.length; i++) {
					var product_items = {
                        'id': orderlines.models[i].product.id,
                        'quantity': orderlines.models[i].quantity,
                        'uom_id': orderlines.models[i].product.uom_id[0],
                        'price': orderlines.models[i].price
                    };
                    
                    pos_product_list.push({'product': product_items });
                }
                
                rpc.query({
		            model: 'pos.create.sales.order',
		            method: 'create_sales_order',
		            args: [partner_id, partner_id.id, pos_product_list],
		            
		            }).then(function(output) {
					alert('Sales Order Created !!!!');	
                    self.gui.show_screen('products');



                });
            });
            //self.button_click();
            
		},
			button_click: function(){},
			highlight: function(highlight){
			this.$el.toggleClass('highlight',!!highlight);
		},
        
        
        
    });

    screens.define_action_button({
        'name': 'Create Sales Order Button Widget',
        'widget': CreateSalesOrderButtonWidget,
        'condition': function() {
            return true;
        },
    });
    // End CreateSalesOrderButtonWidget	
    


	// Start pos_invoice_auto_check
	screens.PaymentScreenWidget.include({
		// Include auto_check_invoice boolean condition in watch_order_changes method
		watch_order_changes: function() {
		    var self = this;
		    var order = this.pos.get_order();
		    
		    if(this.pos.config.auto_check_invoice) // Condition True/False
				{
					var pos_order=this.pos.get_order();
					//console.log("orderrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",pos_order)
					pos_order.set_to_invoice(true);
					this.$('.js_invoice').hide();
				}
			
			
		    if (!order) {
		        return;
		    }
		    if(this.old_order){
		        this.old_order.unbind(null,null,this);
		    }
		    order.bind('all',function(){
		        self.order_changes();
		    });
		    this.old_order = order;
		}
    
    });
    // End pos_invoice_auto_check	
    
        var PosBagWidget = screens.ActionButtonWidget.extend({
        template: 'PosBagWidget',
        
        renderElement: function(){
		    var self = this;
		    this._super();
		    
          	this.$el.click(function(){
          		var selectedOrder = self.pos.get_order();
          		var category = self.pos.config.pos_bag_category_id;
          		var categ = self.pos.db.get_product_by_category(category[0])
          		
	            var products = self.pos.db.get_product_by_category(category[0])[0];
	            
		            
		        //if (product.length == 1) {   
		        if (self.pos.db.get_product_by_category(self.pos.config.pos_bag_category_id[0]).length == 1) { 
		            selectedOrder.add_product(products);
		            //console.log("lasttttttttttttttttttttttt selewcted orderrrrrrrrrrrrrr",selectedOrder)
		        	self.pos.set_order(selectedOrder);
		        	

		        	self.gui.show_screen('products');
                }else{
                	var orderlines = self.pos.db.get_product_by_category(category[0]);
                	self.gui.show_popup('pos_bag_popup_widget', {'orderlines': orderlines});
                }
            	//self.gui.show_popup('pos_bag_popup_widget', {'orderlines': orderlines});

            });
		},
			button_click: function(){},
			highlight: function(highlight){
			this.$el.toggleClass('highlight',!!highlight);
		},
        
        
        
    });

    screens.define_action_button({
        'name': 'Pos Bag Widget',
        'widget': PosBagWidget,
        'condition': function() {
            return true;
        },
    });
    // End CreateSalesOrderButtonWidget	



    // PosBagPopupWidget Popup start

    var PosBagPopupWidget = popups.extend({
        template: 'PosBagPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        
        events: {
            'click .product.bag-category': 'click_on_bag_product',
            'click .button.cancel': 'click_cancel',
        },
        //
        
        get_product_image_url: function(product) {
            return window.location.origin + '/web/binary/image?model=product.product&field=image_medium&id=' + product.id;
        },
        show: function(options) {
        	options = options || {};
            var self = this;
            this._super(options);
            this.orderlines = options.orderlines || [];
            var image_url = this.get_product_image_url(options);

       

        },
        
        click_on_bag_product: function(event) {
            var self = this;
            var bag_id = parseInt($(event.target).parent().data('product-id'))
            //var bag_id = parseInt($(this).parent().data('id'));
            self.pos.get_order().add_product(self.pos.db.product_by_id[bag_id]);
            self.pos.gui.close_popup();
        },


    });
    gui.define_popup({
        name: 'pos_bag_popup_widget',
        widget: PosBagPopupWidget
    });

    // End Popup start
    
    var SelectExistingPopupWidget = popups.extend({
        template: 'SelectExistingPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        //
        show: function(options) {
            var self = this;
            this._super(options);

        },
        //
        renderElement: function() {
            var self = this;
            this._super();
            var order = this.pos.get_order();
            var selectedOrder = self.pos.get('selectedOrder');
            this.$('#apply_coupon_code').click(function() {
                
                var entered_code = $("#existing_coupon_code").val();
                var partner_id = false;
                var coupon_applied = true;
                var used = false;
                if (order.get_client() != null)
                    partner_id = order.get_client();
                rpc.query({
		            model: 'pos.gift.coupon',
		            method: 'existing_coupon',
		            args: [partner_id, entered_code],
                
                }).then(function(output) {
                    var orderlines = order.orderlines;

                    // Popup Occurs when no Customer is selected...
                    if (!partner_id) {
                        self.gui.show_popup('error', {
                            'title': _t('Unknown customer'),
                            'body': _t('You cannot use Coupons/Gift Voucher. Select customer first.'),
                        });
                        return;
                    }

                    // Popup Occurs when not a single product in orderline...
                    if (orderlines.length === 0) {
                        self.gui.show_popup('error', {
                            'title': _t('Empty Order'),
                            'body': _t('There must be at least one product in your order before it can be apply for voucher code.'),
                        });
                        return;
                    }

                    // Goes inside when atleast product in orderline... 	
                    if (orderlines.length) {                	
                        if (output == true) {
                            var selectedOrder = self.pos.get('selectedOrder');
                            selectedOrder.coupon_id = entered_code;
                            var total_amount = selectedOrder.get_total_without_tax();
                            
                            rpc.query({
								model: 'pos.gift.coupon',
								method: 'search_coupon',
								args: [partner_id, entered_code],
						    
						    }).then(function(output) {
                                order.coupon_id = output[0];
                                var amount = output[1];
                                used = output[2];
                                var coupon_count = output[3];
                                var coupon_times = output[4];
                                var expiry = output[5]; 
                                
                                var current_date = new Date().toUTCString();
                                var d = new Date();
                                var month = '' + (d.getMonth() + 1);
                                var day = '' + d.getDate();
								var year = d.getFullYear();
								var date_format = [year, month, day].join('-');
								var hours = d.getHours();
								var minutes = d.getMinutes();
                                var seconds = d.getSeconds();
                                var time_format = [hours, minutes, seconds].join(':');
                                var date_time = [date_format, time_format].join(' ');
                                var partner_true = output[6];
                                var gift_partner_id = output[7];
                                var product_id = self.pos.pos_coupons_setting[0].product_id[0];
                                
                                for (var i = 0; i < orderlines.models.length; i++) {
                                    if (orderlines.models[i].product.id == product_id){
                                        coupon_applied = false;
                                        }
						        }   
						        
						        if (coupon_applied == false) {
						            self.gui.show_popup('error', {
						                'title': _t('Coupon Already Applied'),
						                'body': _t("The Coupon You are trying to apply is already applied in the OrderLines"),
						            });
						        }
                                
                                /*if (date_time > expiry){ // expired
						        	self.gui.show_popup('error', {
						                'title': _t('Expired'),
						                'body': _t("The Coupon You are trying to apply is Expired"),
						            });
						        }*/
						        
						        else if (coupon_count > coupon_times){ // maximum limit
						        	self.gui.show_popup('error', {
						                'title': _t('Maximum Limit Exceeded !!!'),
						                'body': _t("You already exceed the maximum number of limit for this Coupon code"),
						            });
						        }
						        
						        else if (partner_true == true && gift_partner_id != partner_id.id){
								    	self.gui.show_popup('error', {
								            'title': _t('Invalid Customer !!!'),
								            'body': _t("This Gift Coupon is not applicable for this Customer"),
								        });
						        }
                                
                                else { // if coupon is not used
                                
                                var total_val = total_amount - amount;
                                var product_id = self.pos.pos_coupons_setting[0].product_id[0];
                                var product = self.pos.db.get_product_by_id(product_id);
                                var selectedOrder = self.pos.get('selectedOrder');
                                selectedOrder.add_product(product, {
                                    price: -amount
                                });
                                
                             }

                            });
                            self.gui.show_screen('products');
                        } else { //Invalid Coupon Code
                            self.gui.show_popup('error', {
                                'title': _t('Invalid Code !!!'),
                                'body': _t("Voucher Code Entered by you is Invalid. Enter Valid Code..."),
                            });
                        }




                    } else { // Popup Shows, you can't use more than one Voucher Code in single order.
                        self.gui.show_popup('error', {
                            'title': _t('Already Used !!!'),
                            'body': _t("You have already use this Coupon code, at a time you can use one coupon in a Single Order"),
                        });
                    }


                });
            });


        },

    });
    gui.define_popup({
        name: 'select_existing_popup_widget',
        widget: SelectExistingPopupWidget
    });

    // End Popup start


    var GiftButtonWidget = screens.ActionButtonWidget.extend({
        template: 'GiftButtonWidget',
        button_click: function() {
            var order = this.pos.get_order();
            var self = this;
            this.gui.show_popup('select_existing_popup_widget', {});
        },
    });

    screens.define_action_button({
        'name': 'POS Coupens Gift Voucher',
        'widget': GiftButtonWidget,
        'condition': function() {
            return true;
        },
    });
    // End GiftPopupWidget start	



    // Total Items Count in exports.OrderWidget = Backbone.Model.extend ...
    var OrderWidgetExtended = screens.OrderWidget.include({

		update_summary: function(){
		    var order = this.pos.get_order();
		    if (!order.get_orderlines().length) {
		        return;
		    }

		    var total     = order ? order.get_total_with_tax() : 0;
		    var taxes     = order ? total - order.get_total_without_tax() : 0;
		    var total_items    = order ? order.get_total_items() : 0;

		    this.el.querySelector('.summary .total > .value').textContent = this.format_currency(total);
		    this.el.querySelector('.summary .total .subentry .value').textContent = this.format_currency(taxes);
		    this.el.querySelector('.items .value').textContent = total_items;

		},
    });
    


	   

});
