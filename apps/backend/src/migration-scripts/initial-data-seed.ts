import { MedusaContainer } from "@medusajs/framework";
import {
  ContainerRegistrationKeys,
  ModuleRegistrationName,
  Modules,
  ProductStatus,
} from "@medusajs/framework/utils";
import {
  createApiKeysWorkflow,
  createInventoryLevelsWorkflow,
  createProductCategoriesWorkflow,
  createProductsWorkflow,
  createRegionsWorkflow,
  createSalesChannelsWorkflow,
  createShippingOptionsWorkflow,
  createStockLocationsWorkflow,
  createStoresWorkflow,
  createTaxRegionsWorkflow,
  linkSalesChannelsToApiKeyWorkflow,
  linkSalesChannelsToStockLocationWorkflow,
} from "@medusajs/medusa/core-flows";

export default async function initial_data_seed({
  container,
}: {
  container: MedusaContainer;
}) {
  const logger = container.resolve(ContainerRegistrationKeys.LOGGER);
  const link = container.resolve(ContainerRegistrationKeys.LINK);
  const query = container.resolve(ContainerRegistrationKeys.QUERY);
  const fulfillmentModuleService = container.resolve(
    ModuleRegistrationName.FULFILLMENT
  );

  // DIKOROS: украинский рынок, единая валюта UAH, единая страна UA.
  const countries = ["ua"];

  logger.info("Seeding store data...");
  const {
    result: [defaultSalesChannel],
  } = await createSalesChannelsWorkflow(container).run({
    input: {
      salesChannelsData: [
        {
          name: "DIKOROS Storefront",
          description: "Основной канал продаж DIKOROS",
        },
      ],
    },
  });

  const {
    result: [publishableApiKey],
  } = await createApiKeysWorkflow(container).run({
    input: {
      api_keys: [
        {
          title: "DIKOROS Publishable API Key",
          type: "publishable",
          created_by: "",
        },
      ],
    },
  });

  await linkSalesChannelsToApiKeyWorkflow(container).run({
    input: {
      id: publishableApiKey.id,
      add: [defaultSalesChannel.id],
    },
  });

  await createStoresWorkflow(container).run({
    input: {
      stores: [
        {
          name: "DIKOROS",
          supported_currencies: [
            {
              currency_code: "uah",
              is_default: true,
            },
          ],
          default_sales_channel_id: defaultSalesChannel.id,
        },
      ],
    },
  });

  logger.info("Seeding region data...");
  const { result: regionResult } = await createRegionsWorkflow(container).run({
    input: {
      regions: [
        {
          name: "Україна",
          currency_code: "uah",
          countries,
          payment_providers: ["pp_system_default"],
        },
      ],
    },
  });
  const region = regionResult[0];
  logger.info("Finished seeding regions.");

  logger.info("Seeding tax regions...");
  await createTaxRegionsWorkflow(container).run({
    input: countries.map((country_code) => ({
      country_code,
      provider_id: "tp_system",
    })),
  });
  logger.info("Finished seeding tax regions.");
  // Ставку НДС 20% настраиваем в Admin UI вручную после первого запуска.
  // ПДВ платник vs не платник единого налога — открытый вопрос ОВ-7.

  logger.info("Seeding stock location data...");
  const { result: stockLocationResult } = await createStockLocationsWorkflow(
    container
  ).run({
    input: {
      locations: [
        {
          name: "Київський склад",
          address: {
            city: "Київ",
            country_code: "UA",
            address_1: "",
            // Точная точка самовывоза — открытый вопрос ОВ-4 у Юры.
          },
        },
      ],
    },
  });
  const stockLocation = stockLocationResult[0];

  await link.create({
    [Modules.STOCK_LOCATION]: {
      stock_location_id: stockLocation.id,
    },
    [Modules.FULFILLMENT]: {
      fulfillment_provider_id: "manual_manual",
    },
  });

  logger.info("Seeding fulfillment data...");
  const { data: shippingProfileResult } = await query.graph({
    entity: "shipping_profile",
    fields: ["id"],
  });
  const shippingProfile = shippingProfileResult[0];

  const fulfillmentSet = await fulfillmentModuleService.createFulfillmentSets({
    name: "Доставка по Україні",
    type: "shipping",
    service_zones: [
      {
        name: "Україна",
        geo_zones: [
          {
            country_code: "ua",
            type: "country",
          },
        ],
      },
    ],
  });

  await link.create({
    [Modules.STOCK_LOCATION]: {
      stock_location_id: stockLocation.id,
    },
    [Modules.FULFILLMENT]: {
      fulfillment_set_id: fulfillmentSet.id,
    },
  });

  await createShippingOptionsWorkflow(container).run({
    input: [
      {
        name: "Нова Пошта (відділення)",
        price_type: "flat",
        provider_id: "manual_manual",
        service_zone_id: fulfillmentSet.service_zones[0].id,
        shipping_profile_id: shippingProfile.id,
        type: {
          label: "Відділення НП",
          description: "Доставка до відділення Нової Пошти, 1-2 дні",
          code: "nova-poshta-warehouse",
        },
        prices: [
          {
            currency_code: "uah",
            amount: 70,
          },
          {
            region_id: region.id,
            amount: 70,
          },
        ],
        rules: [
          {
            attribute: "enabled_in_store",
            value: "true",
            operator: "eq",
          },
          {
            attribute: "is_return",
            value: "false",
            operator: "eq",
          },
        ],
      },
      {
        name: "Нова Пошта (кур'єр)",
        price_type: "flat",
        provider_id: "manual_manual",
        service_zone_id: fulfillmentSet.service_zones[0].id,
        shipping_profile_id: shippingProfile.id,
        type: {
          label: "Кур'єр НП",
          description: "Адресна доставка кур'єром, 1-2 дні",
          code: "nova-poshta-courier",
        },
        prices: [
          {
            currency_code: "uah",
            amount: 120,
          },
          {
            region_id: region.id,
            amount: 120,
          },
        ],
        rules: [
          {
            attribute: "enabled_in_store",
            value: "true",
            operator: "eq",
          },
          {
            attribute: "is_return",
            value: "false",
            operator: "eq",
          },
        ],
      },
      {
        name: "Самовивіз",
        price_type: "flat",
        provider_id: "manual_manual",
        service_zone_id: fulfillmentSet.service_zones[0].id,
        shipping_profile_id: shippingProfile.id,
        type: {
          label: "Самовивіз",
          description: "Самовивіз з нашого складу в Києві",
          code: "pickup",
        },
        prices: [
          {
            currency_code: "uah",
            amount: 0,
          },
          {
            region_id: region.id,
            amount: 0,
          },
        ],
        rules: [
          {
            attribute: "enabled_in_store",
            value: "true",
            operator: "eq",
          },
          {
            attribute: "is_return",
            value: "false",
            operator: "eq",
          },
        ],
      },
    ],
  });
  logger.info("Finished seeding fulfillment data.");

  await linkSalesChannelsToStockLocationWorkflow(container).run({
    input: {
      id: stockLocation.id,
      add: [defaultSalesChannel.id],
    },
  });
  logger.info("Finished seeding stock location data.");

  logger.info("Seeding product data...");

  const { result: categoryResult } = await createProductCategoriesWorkflow(
    container
  ).run({
    input: {
      product_categories: [
        {
          name: "Гриби",
          handle: "gryby",
          is_active: true,
        },
        {
          name: "Трави",
          handle: "travy",
          is_active: true,
        },
        {
          name: "Мед",
          handle: "med",
          is_active: true,
        },
      ],
    },
  });

  // DEV-DATA: 3 demo-товара, по одному в категорию.
  // Финальный каталог приедет миграцией из Хорошопа в Месяце 2.
  await createProductsWorkflow(container).run({
    input: {
      products: [
        {
          title: "Гриб Чага сушений",
          category_ids: [
            categoryResult.find((cat) => cat.name === "Гриби")!.id,
          ],
          description:
            "Сушений гриб Чага, зібраний у екологічно чистих регіонах України. Класичний адаптоген для щоденного вживання.",
          handle: "hryb-chaha-sushenyy",
          weight: 100,
          status: ProductStatus.PUBLISHED,
          shipping_profile_id: shippingProfile.id,
          images: [
            {
              url: "https://placehold.co/600x600/2d3a1f/ffffff?text=Chaha",
            },
          ],
          options: [
            {
              title: "Фасовка",
              values: ["50 г", "100 г", "200 г"],
            },
          ],
          variants: [
            {
              title: "50 г",
              sku: "DKR-MUSHROOM-CHAHA-50",
              options: { "Фасовка": "50 г" },
              prices: [{ amount: 250, currency_code: "uah" }],
            },
            {
              title: "100 г",
              sku: "DKR-MUSHROOM-CHAHA-100",
              options: { "Фасовка": "100 г" },
              prices: [{ amount: 450, currency_code: "uah" }],
            },
            {
              title: "200 г",
              sku: "DKR-MUSHROOM-CHAHA-200",
              options: { "Фасовка": "200 г" },
              prices: [{ amount: 850, currency_code: "uah" }],
            },
          ],
          sales_channels: [{ id: defaultSalesChannel.id }],
        },
        {
          title: "Іван-чай ферментований",
          category_ids: [
            categoryResult.find((cat) => cat.name === "Трави")!.id,
          ],
          description:
            "Класичний український Іван-чай, ферментований за традиційною технологією. Природний тонізуючий напій без кофеїну.",
          handle: "ivan-chay-fermentovanyy",
          weight: 100,
          status: ProductStatus.PUBLISHED,
          shipping_profile_id: shippingProfile.id,
          images: [
            {
              url: "https://placehold.co/600x600/3d5a2f/ffffff?text=Ivan-Chai",
            },
          ],
          options: [
            {
              title: "Фасовка",
              values: ["50 г", "100 г", "200 г"],
            },
          ],
          variants: [
            {
              title: "50 г",
              sku: "DKR-HERB-IVANCHAI-50",
              options: { "Фасовка": "50 г" },
              prices: [{ amount: 180, currency_code: "uah" }],
            },
            {
              title: "100 г",
              sku: "DKR-HERB-IVANCHAI-100",
              options: { "Фасовка": "100 г" },
              prices: [{ amount: 320, currency_code: "uah" }],
            },
            {
              title: "200 г",
              sku: "DKR-HERB-IVANCHAI-200",
              options: { "Фасовка": "200 г" },
              prices: [{ amount: 600, currency_code: "uah" }],
            },
          ],
          sales_channels: [{ id: defaultSalesChannel.id }],
        },
        {
          title: "Мед липовий",
          category_ids: [
            categoryResult.find((cat) => cat.name === "Мед")!.id,
          ],
          description:
            "Натуральний липовий мед з пасік українського Полісся. Без термообробки та домішок.",
          handle: "med-lypovyy",
          weight: 500,
          status: ProductStatus.PUBLISHED,
          shipping_profile_id: shippingProfile.id,
          images: [
            {
              url: "https://placehold.co/600x600/c4a032/ffffff?text=Honey",
            },
          ],
          options: [
            {
              title: "Об'єм",
              values: ["250 мл", "500 мл", "1 л"],
            },
          ],
          variants: [
            {
              title: "250 мл",
              sku: "DKR-HONEY-LYPA-250",
              options: { "Об'єм": "250 мл" },
              prices: [{ amount: 220, currency_code: "uah" }],
            },
            {
              title: "500 мл",
              sku: "DKR-HONEY-LYPA-500",
              options: { "Об'єм": "500 мл" },
              prices: [{ amount: 400, currency_code: "uah" }],
            },
            {
              title: "1 л",
              sku: "DKR-HONEY-LYPA-1000",
              options: { "Об'єм": "1 л" },
              prices: [{ amount: 750, currency_code: "uah" }],
            },
          ],
          sales_channels: [{ id: defaultSalesChannel.id }],
        },
      ],
    },
  });
  logger.info("Finished seeding product data.");

  logger.info("Seeding inventory levels.");

  const { data: inventoryItems } = await query.graph({
    entity: "inventory_item",
    fields: ["id"],
  });

  await createInventoryLevelsWorkflow(container).run({
    input: {
      inventory_levels: inventoryItems.map((item) => ({
        location_id: stockLocation.id,
        stocked_quantity: 1000000,
        inventory_item_id: item.id,
      })),
    },
  });

  logger.info("Finished seeding inventory levels data.");
}
