/*
 * ECE 461 - Spring 2023 - Project 2
 * API for ECE 461/Spring 2023/Project 2: A Trustworthy Module Registry
 *
 * OpenAPI spec version: 2.0.0
 * Contact: davisjam@purdue.edu
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 *
 * Swagger Codegen version: 3.0.41
 *
 * Do not edit the class manually.
 *
 */
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', '../../src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require('../../src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.Ece461Spring2023Project2);
  }
}(this, function(expect, Ece461Spring2023Project2) {
  'use strict';

  var instance;

  describe('(package)', function() {
    describe('PackageQuery', function() {
      beforeEach(function() {
        instance = new Ece461Spring2023Project2.PackageQuery();
      });

      it('should create an instance of PackageQuery', function() {
        // TODO: update the code to test PackageQuery
        expect(instance).to.be.a(Ece461Spring2023Project2.PackageQuery);
      });

      it('should have the property version (base name: "Version")', function() {
        // TODO: update the code to test the property version
        expect(instance).to.have.property('version');
        // expect(instance.version).to.be(expectedValueLiteral);
      });

      it('should have the property name (base name: "Name")', function() {
        // TODO: update the code to test the property name
        expect(instance).to.have.property('name');
        // expect(instance.name).to.be(expectedValueLiteral);
      });

    });
  });

}));
