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
import {ApiClient} from '../ApiClient';

/**
 * The PackageRegEx model module.
 * @module model/PackageRegEx
 * @version 2.0.0
 */
export class PackageRegEx {
  /**
   * Constructs a new <code>PackageRegEx</code>.
   * A regular expression over package names and READMEs that is used for searching for a package.
   * @alias module:model/PackageRegEx
   * @class
   */
  constructor() {
  }

  /**
   * Constructs a <code>PackageRegEx</code> from a plain JavaScript object, optionally creating a new instance.
   * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
   * @param {Object} data The plain JavaScript object bearing properties of interest.
   * @param {module:model/PackageRegEx} obj Optional instance to populate.
   * @return {module:model/PackageRegEx} The populated <code>PackageRegEx</code> instance.
   */
  static constructFromObject(data, obj) {
    if (data) {
      obj = obj || new PackageRegEx();
    }
    return obj;
  }
}